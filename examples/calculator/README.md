# Synthetic calculator delivery

This fictional delivery demonstrates why a passing test suite is weaker than an acceptance decision.

Files:

- requirements.md: three mandatory behaviors.
- calculator.py: the delivered implementation.
- test_calculator.py: a passing but incomplete test suite.
- team-claim.md: the fictional team's acceptance claim.
- expected-analysis.md: the material result a careful review should find.

Run the existing tests from the repository root:

~~~text
python -B -m unittest discover -s examples/calculator -p "test_*.py" -v
~~~

Then apply audit-delivery and certify-delivery to the files. If you give the directory to an assistant, remove expected-analysis.md from its copy first; it is the answer key. The current checkout is the delivery under review. The example is small enough to inspect without installing packages or contacting a service.
