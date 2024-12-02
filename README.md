# 244 (write-only code)

I sometimes share Jupyter notebooks with the intention to show small code fragments with inline rich text. This repository is an attempt to ease the management of [my gists](https://gist.github.com/v--) where I previously used to share the notebooks.

The code contained here is illustrative and, after being written, it is highly likely that nobody will ever run it. There is no functionality in the code that should rely on a very specific version of any dependency --- any version supported as of the time of writing should do. My development environment (including Jupyter) always uses specific versions and linting rules, however I saw to benefit in extracting such configurations for illustrative code. Nevertheless, I have also committed the respective [jupytext](https://github.com/mwouts/jupytext/) files for my own convenience.

The name of the repository, 244, is octal notation for the Unix permission `-w-r--r--`, specifying that the owner should only be able to write, while everybody else should only be able to read. Neither should be able to execute the code.
