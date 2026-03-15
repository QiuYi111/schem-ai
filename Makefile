PYTHON ?= python
PROJECT_ROOT ?= examples/minimal-repo
TARGET ?= .

.PHONY: bootstrap init status validate review approve-review checkpoint index phase0 phase1 phase2 phase3 phase4 phase5 render

bootstrap:
	$(PYTHON) scripts/bootstrap.py

init:
	$(PYTHON) scripts/init_project.py --target "$(TARGET)"

status:
	$(PYTHON) scripts/status.py --project-root "$(PROJECT_ROOT)"

validate:
	$(PYTHON) scripts/validate.py --project-root "$(PROJECT_ROOT)"

review:
	$(PYTHON) scripts/review.py --project-root "$(PROJECT_ROOT)"

approve-review:
	$(PYTHON) scripts/review.py --project-root "$(PROJECT_ROOT)" --approve

checkpoint:
	$(PYTHON) scripts/checkpoint.py --project-root "$(PROJECT_ROOT)"

index:
	$(PYTHON) scripts/update_index.py --project-root "$(PROJECT_ROOT)"

phase0:
	$(PYTHON) scripts/transition.py phase0 --project-root "$(PROJECT_ROOT)"

phase1:
	$(PYTHON) scripts/transition.py phase1 --project-root "$(PROJECT_ROOT)"

phase2:
	$(PYTHON) scripts/transition.py phase2 --project-root "$(PROJECT_ROOT)"

phase3:
	$(PYTHON) scripts/transition.py phase3 --project-root "$(PROJECT_ROOT)"

phase4:
	$(PYTHON) scripts/transition.py phase4 --project-root "$(PROJECT_ROOT)"

phase5:
	$(PYTHON) scripts/transition.py phase5 --project-root "$(PROJECT_ROOT)"

render:
	$(PYTHON) scripts/render.py --project-root "$(PROJECT_ROOT)"
