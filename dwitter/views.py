# dwitter/views.py

from django.shortcuts import render, redirect
from .models import Profile, Dweet
from . forms import DweetForm


# dwitter/views.py

def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()).order_by('-created_at')
    return render(request, "dwitter/dashboard.html", {"form": form, "dweets": followed_dweets})

# <QueryDict: {'csrfmiddlewaretoken': ['fg8ZBjwKrN7ffm3PzH5RCzj5o8WwESxKzmJBTAuLtaU1KA4r4IUZHoKiefeOljWL'],
# 'body': ['hi i amdahbdyasd\r\n']}> jjjjjjjjjjjjjjjjjjjjjjjjjjjj

# <tr><th></th><td><textarea name="body" cols="40" rows="10" placeholder="Dweet something...."
# class="textarea is-success is-medium" required id="id_body">
# hi i amdahbdyasd
# </textarea></td></tr> rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr


def profile_list(request):
    print(request.user, "oooooooooooooooooooooooooooooooooooo")
    profiles = Profile.objects.exclude(user=request.user)
    print(profiles, "kkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    # In case you haven’t created profiles for you and your existing users you may run into an
    # RelatedObjectDoesNotExist error when performing the POST request.
    # To prevent this error you can verify that your user has a profile in your profile view:

    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == 'POST':
        current_user_profile = request.user.profile
        print(current_user_profile, "ppppppppppppppppppppppppppppppppppp")
        data = request.POST
        action = data.get("follow")
        print(action, "fffffffffffffffffffffffffffffffffffff")
        if action == 'follow':
            current_user_profile.follows.add(profile)
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})
