import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_vector
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt
import io
import plotly.graph_objects as go
from PIL import Image

st.title("3D Bloch Sphere Simulator 🎲")
st.write("Follow me on GitHub: [https://github.com/wahidpanda](https://github.com/wahidpanda)")

# Quantum circuit to visualize Bloch vector
qc = QuantumCircuit(1)

# User input for quantum gates
st.sidebar.subheader("Quantum Gate")

gate = st.sidebar.selectbox("Select Quantum Gate", ["I", "X", "Y", "Z", "H", "S", "T"])

# Define gate descriptions
gate_descriptions = {
    "I": "Identity Gate (No change):\n"
          "The Identity gate, denoted as I, does not alter the state of the qubit. "
          "It is effectively a 'do nothing' operation, leaving the qubit in its current state.",
    "X": "Pauli-X Gate (Bit-flip):\n"
          "The Pauli-X gate, represented as X, flips the state of the qubit, "
          "changing |0> to |1> and |1> to |0>. It's also known as the 'bit-flip' gate.",
    "Y": "Pauli-Y Gate:\n"
          "The Pauli-Y gate, denoted as Y, performs a combination of bit-flip and phase-flip operations. "
          "It transforms |0> to i|1> and |1> to -i|0>. It is often used in various quantum algorithms.",
    "Z": "Pauli-Z Gate (Phase-flip):\n"
          "The Pauli-Z gate, represented as Z, only affects the phase of the qubit. "
          "It leaves |0> unchanged and adds a phase of π (180 degrees) to |1>. It's the 'phase-flip' gate.",
    "H": "Hadamard Gate:\n"
          "The Hadamard gate, denoted as H, creates superposition. It maps |0> to (|0> + |1>)/√2 "
          "and |1> to (|0> - |1>)/√2, effectively putting the qubit into an equal superposition state.",
    "S": "S Gate (Phase Gate):\n"
          "The S gate, represented as S, applies a 90-degree phase shift to |1>. "
          "It transforms |0> to |0> and |1> to i|1>. It is commonly used for creating quantum interference.",
    "T": "T Gate (T Phase Gate):\n"
          "The T gate, denoted as T, introduces a π/4 (45-degree) phase shift to |1>. "
          "It transforms |0> to |0> and |1> to (|0> + i|1>)/√2. It's important in quantum algorithms like Shor's."
}

if gate == "X":
    qc.x(0)
elif gate == "Y":
    qc.y(0)
elif gate == "Z":
    qc.z(0)
elif gate == "H":
    qc.h(0)
elif gate == "S":
    qc.s(0)
elif gate == "T":
    qc.t(0)

# Simulate the quantum circuit
backend = Aer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()
state_vector = result.get_statevector()

# Bloch vector components
x = np.real(state_vector[0])
y = np.real(state_vector[1])
z = 0  # The z-component is always 0 for a single-qubit Bloch vector

# Create Bloch sphere plot
bloch_fig = go.Figure()


# Add Bloch vector
bloch_fig.add_trace(
    go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers', marker=dict(size=10, color='red'),
                  line=dict(width=5), name="Bloch Vector")
)

# Add Bloch sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
radius = 1.5  # Increase the radius for a larger sphere
x_sphere = radius * np.outer(np.cos(u), np.sin(v))
y_sphere = radius * np.outer(np.sin(u), np.sin(v))
z_sphere = radius * np.outer(np.ones(np.size(u)), np.cos(v))
bloch_fig.add_trace(go.Surface(x=x_sphere, y=y_sphere, z=z_sphere, colorscale='Oranges', opacity=0.5, showscale=False))

bloch_fig.update_layout(scene=dict(
    xaxis_title='X',
    yaxis_title='Y',
    zaxis_title='Z',
    aspectmode="data"
))

st.plotly_chart(bloch_fig, use_container_width=True)

# Display gate description and circuit diagram
st.subheader("Gate Description")
if gate in gate_descriptions:
    st.write(gate_descriptions[gate])

st.subheader("Circuit Diagram")

circuit = QuantumCircuit(1)
if gate == "X":
    circuit.x(0)
elif gate == "Y":
    circuit.y(0)
elif gate == "Z":
    circuit.z(0)
elif gate == "H":
    circuit.h(0)
elif gate == "S":
    circuit.s(0)
elif gate == "T":
    circuit.t(0)

# Generate the circuit diagram image with a transparent background
# Generate the circuit diagram image with a transparent background
# Generate the circuit diagram image with a transparent background using the "clifford" style
image = io.BytesIO()
fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
circuit_drawer(circuit, output='mpl', style='clifford', ax=ax)
ax.patch.set_facecolor('none')  # Set the background color to transparent
fig.savefig(image, format='png', bbox_inches='tight', transparent=True)
st.image(image, use_column_width=True)



st.sidebar.subheader("Bloch Vector")

# Display Bloch vector coordinates
st.sidebar.write(f"x: {x}")
st.sidebar.write(f"y: {y}")
st.sidebar.write(f"z: {z}")

st.sidebar.write("Note: The Bloch sphere is a 3D representation of the state of a single qubit.")
