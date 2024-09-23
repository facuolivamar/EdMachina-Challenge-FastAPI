// src/App.tsx

import React from 'react';
import RegistroForm from './components/RegistroForm';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>Formulario de Registro</h1>
      <RegistroForm />
    </div>
  );
};

export default App;
