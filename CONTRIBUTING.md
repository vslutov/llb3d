# Contributing

We love pull requests from everyone. By participating in this project, you
agree to abide by the thoughtbot [code of conduct].

[code of conduct]: CODE_OF_CONDUCT.md

Fork, then clone the repo:

    git clone git@github.com:your-username/llb3d.git

Set up your machine:

    apt install cmake libicu-dev
    python setup.py develop
    pip install -e ".[dev]"

Make sure the tests pass:

    pytest llb3d

Make your change. Add tests for your change. Make the tests pass:

    pytest llb3d
    pylint llb3d

Push to your fork and [submit a pull request][pr].

[pr]: https://github.com/vslutov/llb3d/compare/

At this point you're waiting on us. We like to at least comment on pull requests
within three business days (and, typically, one business day). We may suggest
some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted:

* Write tests.
* Follow [style guide PEP 8][style].
* Write a [good commit message][commit].

[style]: https://www.python.org/dev/peps/pep-0008/
[commit]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
