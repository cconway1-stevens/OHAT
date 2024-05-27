import React, { useState } from 'react';
import { useTireBrandsContext } from '../src/context/TireBrandsContext';
import NavBar from '../src/components/NavBar';

const ManageBrands = () => {
  const { brands, addBrand, removeBrand } = useTireBrandsContext();
  const [newBrand, setNewBrand] = useState('');

  const handleAddBrand = () => {
    if (newBrand && !brands.includes(newBrand)) {
      addBrand(newBrand);
      setNewBrand('');
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <NavBar />
      <main className="flex flex-col items-center justify-center p-4 bg-gray-100 flex-grow">
        <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
          <h1 className="text-3xl font-bold mb-6 text-center">Manage Tire Brands</h1>
          <div className="flex flex-col mb-6">
            <input
              type="text"
              placeholder="New Brand"
              value={newBrand}
              onChange={(e) => setNewBrand(e.target.value)}
              className="p-2 mb-4 border border-gray-300 rounded"
            />
            <button
              className="p-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 transition"
              onClick={handleAddBrand}
            >
              Add Brand
            </button>
          </div>
          <ul className="list-none p-0">
            {brands.map((brand) => (
              <li key={brand} className="flex justify-between items-center mb-2">
                <span className="text-lg">{brand}</span>
                <button
                  className="p-2 bg-red-500 text-white rounded shadow hover:bg-red-600 transition"
                  onClick={() => removeBrand(brand)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>
      </main>
    </div>
  );
};

export default ManageBrands;
