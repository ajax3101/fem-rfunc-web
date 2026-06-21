import os
from flask import Flask, request, jsonify

import sys
# Make sure the app can import legacy_fem modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fem_object import TObject
from fem_error import TFEMException

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "Welcome to the Legacy FEM API"
    })

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    obj = TObject()

    mesh_path = data.get('mesh_path')
    if not mesh_path:
        return jsonify({"error": "mesh_path is required"}), 400

    # Optional parameters fallback
    problem_type = data.get('problem_type', 'static')
    solve_method = data.get('solve_method', 'direct')
    e = data.get('elasticity', [2.0E+11])
    m = data.get('poisson_ratio', [0.3])

    # Try to resolve full path, assuming it is given relative to legacy_fem directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    full_mesh_path = os.path.join(base_dir, mesh_path)

    if not os.path.exists(full_mesh_path):
         return jsonify({"error": f"Mesh file not found at {full_mesh_path}"}), 404

    try:
        obj.set_mesh(full_mesh_path)
        obj.set_problem_type(problem_type)
        obj.set_solve_method(solve_method)
        obj.set_elasticity(e, m)

        boundaries = data.get('boundary_conditions', [])
        for bc in boundaries:
            obj.add_boundary_condition(bc.get('e', '0'), bc.get('p'), bc.get('d'))

        surface_loads = data.get('surface_loads', [])
        for sl in surface_loads:
            obj.add_surface_load(sl.get('e'), sl.get('p'), sl.get('d'))

        volume_loads = data.get('volume_loads', [])
        for vl in volume_loads:
            obj.add_volume_load(vl.get('e'), vl.get('p'), vl.get('d'))

        conc_loads = data.get('concentrated_loads', [])
        for cl in conc_loads:
            obj.add_concentrated_load(cl.get('e'), cl.get('p'), cl.get('d'))

        success = obj.calc()

        if not success:
            return jsonify({"error": "Calculation failed"}), 500

        # Serialize some output results
        res_data = []
        # obj.__results__ contains TResult items which have min/max and the list of nodal values
        for r in obj.__results__:
            res_data.append({
                "name": r.name,
                "min": r.min(),
                "max": r.max(),
                # "results": r.results  # Omitted full array to avoid giant payload by default
            })

        return jsonify({
            "status": "success",
            "results": res_data
        })

    except TFEMException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
