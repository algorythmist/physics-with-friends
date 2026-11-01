# Physics and Friends

This project contains problem solutions, notes, and presentations from the Meetup 
"Physics with Friends".

The solutions can be in pure latex, jupyter notebook format, pdf, matlab 
or any other format.

---

## Instructions for running locally

1. Install Python or Anaconda
2. Create a venv or conda environment
3. Install requirements.txt (mainly for plots)
4. Start a jupyter notebook 

### Interactive 3D parametric curves

Run `python src/parametric_curve_3d.py` to open the curve visualizer. Enter
expressions for `x(t)`, `y(t)`, and `z(t)`, set the parameter range, and select
**Draw**. Expressions support arithmetic, `t`, `pi`, `e`, and common functions
such as `sin`, `cos`, `sqrt`, `exp`, `log`, and `abs`.

For the browser-based Plotly version, install `requirements.txt` and run
`python src/parametric_curve_plotly.py`. Open the local URL printed in the
terminal to enter expressions and explore the interactive 3D graph.

## Instructions for Collaborators

1. Send me your GitHub handle and I will add you as a collaborator
2. Checkout the project
3. Follow the instructions for running locally
4. If a chapter does not exist, create a new Jupyter notebook for it. 
5. If the chapter exists, and you want to add a new problem, add it to the existing notebook.
6. If the chapter exists and the problem has a solution, you can request a review to your solution or add it as an alternative solution.
7. If you prefer pure Latex to Jupyter notebooks, you can add .tex files under the "latex" directory. Please place the compiled PDFs under the pdf directory.
