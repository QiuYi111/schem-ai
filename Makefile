PYTHON ?= python

.PHONY: bootstrap init status validate review checkpoint index phase0 phase1 phase2 phase3 phase4 phase5 render

bootstrap:
	 scripts/bootstrap.py

init:
	 scripts/init_project.py

status:
	 scripts/status.py

validate:
	 scripts/validate.py

review:
	 scripts/review.py

checkpoint:
	 scripts/checkpoint.py

index:
	 scripts/update_index.py

phase0:
	 scripts/transition.py phase0

phase1:
	 scripts/transition.py phase1

phase2:
	 scripts/transition.py phase2

phase3:
	 scripts/transition.py phase3

phase4:
	 scripts/transition.py phase4

phase5:
	 scripts/transition.py phase5

render:
	 scripts/render.py
