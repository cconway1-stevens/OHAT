import React, { createContext, useContext, useState } from 'react';

const TireBrandsContext = createContext();

export const useTireBrandsContext = () => useContext(TireBrandsContext);

export const TireBrandsProvider = ({ children }) => {
  const [brands, setBrands] = useState([
    'Michelin',
    'Goodyear',
    'Bridgestone',
    'Pirelli',
    'Continental',
    'Dunlop',
    'Yokohama',
    'Hankook',
    'Toyo',
    'Cooper',
  ]);

  const addBrand = (brand) => {
    setBrands([...brands, brand]);
  };

  const removeBrand = (brand) => {
    setBrands(brands.filter((b) => b !== brand));
  };

  return (
    <TireBrandsContext.Provider value={{ brands, addBrand, removeBrand }}>
      {children}
    </TireBrandsContext.Provider>
  );
};
