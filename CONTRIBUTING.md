# Contributing to pkg-rpm-qcom-video-ctrl

Thank you for your interest in contributing to this project. Contributions
that improve the RPM metadata, packaging workflows, or project documentation
are welcome.

## Branching strategy

This repository follows the Fedora/CentOS dist-git branch model:

- `main` contains repository documentation and workflow support files.
- `c10s` contains the CentOS 10 Stream package spec and `sources` file.

Target documentation and workflow changes at `main`. Target package and spec
changes at `c10s`.

## Submitting a pull request

1. Read the [code of conduct](CODE-OF-CONDUCT.md) and
   [license](LICENSE.txt).
2. Fork and clone the repository:

   ```bash
   git clone https://github.com/qualcomm-linux/pkg-rpm-qcom-video-ctrl.git
   cd pkg-rpm-qcom-video-ctrl
   ```

3. Create a topic branch from the branch you intend to update:

   ```bash
   git checkout -b <my-branch-name> <target-branch>
   ```

4. Add an upstream remote so you can keep your branch synchronized:

   ```bash
   git remote add upstream https://github.com/qualcomm-linux/pkg-rpm-qcom-video-ctrl.git
   ```

5. Make the change. For package changes, keep the spec and `sources` file in
   sync and use the pull-request build to verify the RPM.
6. Commit using the Developer Certificate of Origin (DCO) sign-off:

   ```bash
   git commit -s -m "Describe the change"
   ```

7. Rebase your topic branch on the target branch before submitting it:

   ```bash
   git pull --rebase upstream <target-branch>
   ```

8. Push the branch to your fork:

   ```bash
   git push -u origin <my-branch-name>
   ```

9. Open a pull request against the appropriate target branch. Keep each pull
   request focused on one logical change.

## Security analysis of pull requests

Pull requests from external contributors may be automatically scanned with
[Semgrep](https://semgrep.dev/) to identify insecure patterns and potential
security issues.

If the analysis reports an issue, resolve it or explain the finding before the
pull request is merged. The ruleset may evolve as security guidance and known
risks change.

## Contribution guidelines

- Follow the existing documentation and RPM spec style.
- Keep changes focused; submit independent changes as separate pull requests.
- Update documentation when behavior, packaging requirements, or workflows
  change.
- Include relevant validation results in the pull request description.
- Use a clear commit message; see [A Note About Git Commit
  Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
  for guidance.
