# Smart Attendance Android project

This folder contains a Python/Kivy attendance calculator prepared for Android packaging.

## What's included
- `main.py` — the mobile app.
- `background.jpg` — your supplied photo used as the app background.
- `buildozer.spec` — Android packaging configuration.
- `.github/workflows/build-apk.yml` — optional cloud build workflow using GitHub Actions.

## Easiest cloud build (no Linux setup on your own computer)
1. Create/sign in to a GitHub account.
2. Create a new repository.
3. Upload all files and folders from this ZIP (including the hidden `.github` folder).
4. Open the repository's **Actions** tab.
5. If prompted, enable Actions for the repository.
6. Select **Build Android APK** on the left, then click **Run workflow**.
7. Wait for the workflow to finish successfully.
8. Open the completed run and download the **Smart-Attendance-APK** artifact.
9. Extract the downloaded artifact ZIP. It contains the `.apk` file.
10. Transfer the APK to your Android phone and open it to install. Android may ask you to allow installs from that source.

## Build locally
On Ubuntu or WSL with Java 17 and Buildozer installed, run:
`buildozer android debug`

## Notes
- This project produces a debug APK for personal testing, not a Play Store release.
- The app assumes each future working day is either present or absent.
- The absence allowance is calculated to stay at or above the selected target.
- No internet permission or account login is required by this app.
