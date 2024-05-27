import React, { createContext, useContext, useState } from 'react';

const TireContext = createContext();

export const useTireContext = () => useContext(TireContext);

export const TireProvider = ({ children }) => {
  const [tires, setTires] = useState([]);
  const [variables, setVariables] = useState({
    tax: 6.625,
    surcharge: 5.0,
    tireMarkUp: 67.0,
    njTireTax: 1.5,
    disposalFee: 7.0,
  });

  const addTire = (tire) => {
    setTires([...tires, tire]);
  };

  const undoLastTire = () => {
    setTires(tires.slice(0, -1));
  };

  const clearAllTires = () => {
    setTires([]);
  };

  const removeTire = (index) => {
    setTires(tires.filter((_, i) => i !== index));
  };

  return (
    <TireContext.Provider value={{ tires, variables, setVariables, addTire, undoLastTire, clearAllTires, removeTire }}>
      {children}
    </TireContext.Provider>
  );
};
