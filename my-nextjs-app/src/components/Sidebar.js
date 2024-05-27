import React, { useState } from 'react';
import { useTireContext } from '../context/TireContext';
import { useTireBrandsContext } from '../context/TireBrandsContext';

const Sidebar = () => {
  const { variables, setVariables, addTire, undoLastTire, clearAllTires } = useTireContext();
  const { brands } = useTireBrandsContext();
  const [tireName, setTireName] = useState('');
  const [tireCost, setTireCost] = useState('');
  const [selectedBrand, setSelectedBrand] = useState('');

  const handleAddTire = () => {
    addTire({ name: selectedBrand, cost: parseFloat(tireCost) });
    setSelectedBrand('');
    setTireCost('');
  };

  return (
    <div className="p-4 bg-gray-200 h-full">
      <h2 className="text-xl font-semibold mb-4">Add Tire</h2>
      <div className="flex flex-col mb-6">
        <select
          value={selectedBrand}
          onChange={(e) => setSelectedBrand(e.target.value)}
          className="p-2 mb-2 border border-gray-300 rounded"
        >
          <option value="" disabled>Select Brand</option>
          {brands.map((brand) => (
            <option key={brand} value={brand}>
              {brand}
            </option>
          ))}
        </select>
        <input
          type="number"
          placeholder="Cost"
          value={tireCost}
          onChange={(e) => setTireCost(e.target.value)}
          className="p-2 mb-2 border border-gray-300 rounded"
        />
        <button
          className="p-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 transition"
          onClick={handleAddTire}
        >
          Add Tire
        </button>
      </div>

      <h2 className="text-xl font-semibold mb-4">Variables</h2>
      <div className="flex flex-col">
        {Object.entries(variables).map(([key, value]) => (
          <div key={key} className="flex flex-col mb-4">
            <label className="mb-1 text-sm font-medium capitalize">{key.replace(/([A-Z])/g, ' $1')}</label>
            <input
              type="number"
              value={value}
              onChange={(e) => setVariables({ ...variables, [key]: parseFloat(e.target.value) })}
              className="p-2 border border-gray-300 rounded"
            />
          </div>
        ))}
      </div>
      
      <button
        className="p-2 bg-red-500 text-white rounded shadow hover:bg-red-600 transition mb-2"
        onClick={undoLastTire}
      >
        Undo Last Tire
      </button>
      <button
        className="p-2 bg-yellow-500 text-white rounded shadow hover:bg-yellow-600 transition"
        onClick={clearAllTires}
      >
        Clear All Tires
      </button>
    </div>
  );
};

export default Sidebar;
