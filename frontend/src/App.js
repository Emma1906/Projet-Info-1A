import React, { useState } from "react";
import axios from "axios";

function App() {
  const [pilotes, setPilotes] = useState([{ age: 25, points: 100 }]);
  const [resultats, setResultats] = useState([]);

  const handleChange = (index, field, value) => {
    const updated = [...pilotes];
    updated[index][field] = Number(value);
    setPilotes(updated);
  };

  const ajouterPilote = () => {
    setPilotes([...pilotes, { age: 0, points: 0 }]);
  };

  const envoyer = async () => {
    try {
      const res = await axios.post("http://localhost:5000/predict", pilotes);
      setResultats(res.data.predictions);
    } catch (err) {
      console.error("Erreur :", err);
    }
  };

  return (
    <div>
      <h1>Simulation de podium</h1>
      {pilotes.map((pilote, index) => (
        <div key={index}>
          <input
            type="number"
            value={pilote.age}
            onChange={(e) => handleChange(index, "age", e.target.value)}
            placeholder="Âge"
          />
          <input
            type="number"
            value={pilote.points}
            onChange={(e) => handleChange(index, "points", e.target.value)}
            placeholder="Points"
          />
        </div>
      ))}
      <button onClick={ajouterPilote}>Ajouter un pilote</button>
      <button onClick={envoyer}>Prédire</button>

      <ul>
        {resultats.map((res, i) => (
          <li key={i}>
            Pilote {i + 1} {res === 1 ? "sera" : "ne sera pas"} sur le podium
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
