// src/components/SpreadsheetTable.js
import React, { useState } from 'react';
import Spreadsheet from 'react-spreadsheet';
import styles from '../styles/SpreadsheetTable.module.css';

const SpreadsheetTable = () => {
  const [variables, setVariables] = useState({
    tax: 6.625,
    surcharge: 5.0,
    tireMarkUp: 67.0,
    njTireTax: 1.5,
    disposalFee: 7.0,
  });
  const [costRange, setCostRange] = useState({ start: 40, end: 100, step: 5 });
  const [data, setData] = useState([]);

  const handleVariableChange = (key, value) => {
    setVariables({ ...variables, [key]: parseFloat(value) });
  };

  const handleCostRangeChange = (key, value) => {
    setCostRange({ ...costRange, [key]: parseFloat(value) });
  };

  const calculateRow = (cost) => {
    const { tax, surcharge, tireMarkUp, njTireTax, disposalFee } = variables;
    const fees = tireMarkUp + njTireTax + disposalFee + surcharge;
    const totalWithTax = (cost + fees) * (1 + tax / 100);
    return {
      cost,
      fees: fees.toFixed(2),
      totalWithTax: totalWithTax.toFixed(2),
      total1: (totalWithTax * 1).toFixed(2),
      total2: (totalWithTax * 2).toFixed(2),
      total3: (totalWithTax * 3).toFixed(2),
      total4: (totalWithTax * 4).toFixed(2),
    };
  };

  const generateTableData = () => {
    const rows = [];
    for (let cost = costRange.start; cost <= costRange.end; cost += costRange.step) {
      const row = calculateRow(cost);
      rows.push([
        { value: `$${row.cost}` },
        { value: `$${row.fees}` },
        { value: `$${row.totalWithTax}` },
        { value: `$${row.total1}` },
        { value: `$${row.total2}` },
        { value: `$${row.total3}` },
        { value: `$${row.total4}` },
      ]);
    }
    const header = [
      { value: "Cost" },
      { value: "Fees" },
      { value: "W/tax" },
      { value: "1 Tire" },
      { value: "2 Tires" },
      { value: "3 Tires" },
      { value: "4 Tires" },
    ];
    setData([header, ...rows]);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="container mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-3xl font-bold mb-6 text-center">Tire Pricing Estimator</h1>
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Variables</h2>
        <div className="grid grid-cols-2 gap-4 mb-6">
          {Object.entries(variables).map(([key, value]) => (
            <div key={key} className="flex flex-col">
              <label className="mb-1 text-sm font-medium capitalize">{key.replace(/([A-Z])/g, ' $1')}</label>
              <input
                type="number"
                value={value}
                onChange={(e) => handleVariableChange(key, e.target.value)}
                className="p-2 border border-gray-300 rounded"
              />
            </div>
          ))}
        </div>
        <h2 className="text-xl font-semibold mb-4">Cost Range</h2>
        <div className="grid grid-cols-3 gap-4 mb-6">
          {Object.entries(costRange).map(([key, value]) => (
            <div key={key} className="flex flex-col">
              <label className="mb-1 text-sm font-medium capitalize">{key}</label>
              <input
                type="number"
                value={value}
                onChange={(e) => handleCostRangeChange(key, e.target.value)}
                className="p-2 border border-gray-300 rounded"
              />
            </div>
          ))}
        </div>
        <div className="flex space-x-4">
          <button
            className="p-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 transition"
            onClick={generateTableData}
          >
            Generate Table
          </button>
          <button
            className="p-2 bg-green-500 text-white rounded shadow hover:bg-green-600 transition"
            onClick={handlePrint}
          >
            Print Table
          </button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <Spreadsheet data={data} className={styles.spreadsheet} />
      </div>
    </div>
  );
};

export default SpreadsheetTable;
