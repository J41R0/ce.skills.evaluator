## Making Changes

- Make sure you are going to resolve a registered issue.

  - If there is an issue registered, it should be well described and estimated before you start working on it.
  - If there is not an issue registered, please register a new issue, add the description and the estimations before you start working on it.

- Create a topic branch from where you want to base your work.

  - This is usually from the _development_ branch.
  - To quickly create a topic branch based on master, run `git checkout -b <feature/my_feature_name> <development>`. Please avoid working directly on the _master_ or _development_ branches.

- Move the issue to _In Progress_ column.

- Make commits of logical and atomic units.

- Make sure your commit messages are in the proper format:

  > Commit header including the number of the issue you are solving _ex. (#55)_

  > Commit description _(only if it is needed)_

- Before push your commits make sure you have added the necessary tests for your changes, and you run all the project tests.

## Submitting Changes

- Push your changes to the topic branch.

- Move the issue|task to _In Review_ column.

- After the team approve the task:

  - Move to the parent branch `git checkout <development>` and run `git pull <remote_name> <development>`.
  - Move to your topic branch and run `git rebase <development>`.
  - Solve all conflicts.
  - Move to the parent branch `git checkout <development>` and run `git merge --no-ff <feature/my_feature_name>`.
  - Update the milestone in the task issue to the current month milestone.
  - Move the issue task to _Closed_ column.
  - Delete the topic branch in the remote host `git push --delete <remote_name> <feature/my_feature_name>`.
  - Delete the topic branch locally `git branch -d <feature/my_feature_name>`.

- If the team reject the solution:

  - Move the issue to _In Progress_ column.
  - Solve the reviewer comments.
  - Move the issue task to _In Review_ column.

## Testing your code

- Make sure to have a test coverage of at least _80%_ in each new code before pushing it.

## Folder structure

```
├── evaluator
│  ├── api
│  │   ├── dto
│  │   └── resources
│  ├── app
│  └── domain
│      └── resources
└── tests
