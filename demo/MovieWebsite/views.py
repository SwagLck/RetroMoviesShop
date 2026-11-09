from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, TvShow, Comment, Report
from .forms import ProfileForm, UserForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count, Q
from .models import Genre

# Create your views here.
def home(request):
    return render(request, "home.html")

def admin_panel(request):
    return render(request, "admin_panel.html")

def discount_add(request):
    return render(request, "discount_add.html")

def history(request):
    return render(request, "history.html")

def order(request):
    return render(request, "order.html")

def subscriptions(request):
    return render(request, "subscriptions.html")

def movies(request):
    items = Movie.objects.prefetch_related("genres").order_by("-year", "title")
    page = Paginator(items, 24).get_page(request.GET.get("page"))
    return render(request, "movies.html", {"movies": page, "page_obj": page})


def tvshows(request):
    items = TvShow.objects.prefetch_related("genres").order_by("-year", "title")
    page = Paginator(items, 24).get_page(request.GET.get("page"))
    return render(request, "tvshows.html", {"tvshows": page, "page_obj": page})



def movie_detail(request, pk):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("genres"),
        pk=pk
    )

    already_reviewed = False

    if request.user.is_authenticated:
        already_reviewed = Comment.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        if already_reviewed:
            messages.error(
                request,
                "You have already reviewed this movie."
            )
            return redirect("movie_detail", pk=movie.pk)

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()

            return redirect("movie_detail", pk=movie.pk)
    else:
        form = CommentForm()

    comments = movie.comments.select_related("user")

    return render(request, "movie_detail.html", {
        "movie": movie,
        "comments": comments,
        "form": form,
        "already_reviewed": already_reviewed,
    })


def tvshow_detail(request, pk):
    tvshow = get_object_or_404(TvShow.objects.prefetch_related("genres"), pk=pk)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tvshow = tvshow
            comment.save()
            return redirect("tvshow_detail", pk=tvshow.pk)
    else:
        form = CommentForm()

    comments = tvshow.comments.select_related("user")
    return render(request, "tvshow_detail.html", {
        "tvshow": tvshow,
        "comments": comments,
        "form": form,
    })

@login_required
@user_passes_test(lambda u: u.is_staff or u.has_perm("MovieWebsite.can_block_users"))
def userslist(request):
    users = User.objects.all()
    return render(request, "userslist.html", {"users": users})

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username = username)

    user_profile = profile_user.profile

    return render(request, "profile.html", {
        "profile_user": profile_user,
        "profile": user_profile,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile", username=request.user.username)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
@require_POST
def toggle_block_user(request, username):
    if not request.user.has_perm("MovieWebsite.can_block_users"):
        raise PermissionDenied

    target = get_object_or_404(User, username=username)

    if target == request.user:
        messages.error(request, "You cannot block yourself.")
    elif target.is_superuser or target.groups.filter(name="Moderator").exists():
        messages.error(request, "You cannot block this user.")
    else:
        target.is_active = not target.is_active
        target.save(update_fields=["is_active"])
        state = "unblocked" if target.is_active else "blocked"
        messages.success(request, f"User {target.username} has been {state}.")

    return redirect("profile", username=username)


def _can_moderate(user):
    return user.is_staff or user.has_perm("MovieWebsite.can_block_users")


def _back_to_item(comment):
    if comment.movie_id:
        return redirect("movie_detail", pk=comment.movie_id)
    return redirect("tvshow_detail", pk=comment.tvshow_id)


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        raise PermissionDenied

    comment.delete()
    messages.success(request, "Comment deleted")
    return _back_to_item(comment)

@login_required
@require_POST
def toggle_hide_comment(request, pk):
    if not _can_moderate(request.user):
        raise PermissionDenied

    comment = get_object_or_404(Comment, pk=pk)
    comment.is_hidden= not comment.is_hidden
    comment.save(update_fields=["is_hidden"])

    state = "hidden" if comment.is_hidden else "visible again"
    messages.success(request, f"Comment is now {state}.")
    return _back_to_item(comment)

@login_required
@require_POST
def report_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user == request.user:
        messages.error(request, "You can't report your own comment.")
    else:
        _, created = Report.objects.get_or_create(comment=comment, reporter=request.user)
        if created:
            messages.success(request, "Thanks, the comment has been reported")
        else:
            messages.info(request, "You have already reported this comment")

    return _back_to_item(comment)


@login_required
def reports_list(request):
    if not _can_moderate(request.user):
        raise PermissionDenied

    reports = Report.objects.select_related(
        "reporter", "comment__user", "comment__movie", "comment__tvshow"
    )
    return render(request, "reports.html", {"reports": reports})


def movie_statistics(request):
    movies = Movie.objects.all()

    genre = request.GET.get("genre", "")
    year = request.GET.get("year", "")
    min_rating = request.GET.get("min_rating", "")
    min_count = request.GET.get("min_count", "")

    if genre.isdigit():
        movies = movies.filter(genres__id=int(genre))

    if year.isdigit():
        movies = movies.filter(year=int(year))

    movies = movies.annotate(
        average_rating=Avg(
            "comments__rating",
            filter=Q(comments__is_hidden=False)
        ),
        rating_count=Count(
            "comments",
            filter=Q(
                comments__is_hidden=False,
                comments__rating__isnull=False
            )
        )
    ).filter(rating_count__gt=0)

    try:
        if min_rating:
            movies = movies.filter(
                average_rating__gte=float(min_rating)
            )
    except ValueError:
        pass

    if min_count.isdigit():
        movies = movies.filter(
            rating_count__gte=int(min_count)
        )

    movies = movies.order_by("-average_rating", "title")

    return render(request, "movie_statistics.html", {
        "movies": movies,
        "genres": Genre.objects.order_by("name"),
        "selected_genre": genre,
        "selected_year": year,
        "selected_rating": min_rating,
        "selected_count": min_count,
    })
    
@login_required
@require_POST
def edit_comment(request, pk):
    comment = get_object_or_404(
        Comment,
        pk=pk,
        user=request.user
    )

    form = CommentForm(request.POST, instance=comment)

    if form.is_valid():
        form.save()
        messages.success(request, "Review updated successfully.")
    else:
        messages.error(request, "Could not update review. Check your input.")

    if comment.movie_id:
        return redirect("movie_detail", pk=comment.movie_id)

    if comment.tvshow_id:
        return redirect("tvshow_detail", pk=comment.tvshow_id)

    return redirect("home")
