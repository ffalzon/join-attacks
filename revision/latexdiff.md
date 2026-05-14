# Generating latexdiff
1. Copy git revision `1c21d74a87103dfde2ab64641941535fc0dd4dfe` into folder `pre_revision`
3. In repository root directory, run `latexdiff --flatten revision/pre_revision/main.tex main.tex > diff.tex`
4. Compile `diff.tex` in repository root directory