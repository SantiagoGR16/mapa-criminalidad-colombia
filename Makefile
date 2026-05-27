.PHONY: install ingest transform enrich pipeline dashboard test lint clean

install:
	pip install -r requirements.txt

ingest:
	python -m src.ingest

transform:
	python -m src.transform

enrich:
	python -m src.enrich

pipeline: ingest transform enrich

dashboard:
	streamlit run dashboard/app.py

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/ --max-line-length=120
	flake8 dashboard/ --max-line-length=120

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
