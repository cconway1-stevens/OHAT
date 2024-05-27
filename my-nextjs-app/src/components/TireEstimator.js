import React from 'react';
import { useTireContext } from '../context/TireContext';
import styles from '../styles/Print.module.css';

const TireEstimator = () => {
  const { tires, variables, removeTire } = useTireContext();

  const calculateClientCost = (cost) => {
    const { tax, surcharge, tireMarkUp, njTireTax, disposalFee } = variables;
    const fees = tireMarkUp + njTireTax + disposalFee + surcharge;
    const totalWithTax = (cost + fees) * (1 + tax / 100);
    return totalWithTax.toFixed(2);
  };

  const generateEstimate = () => {
    return tires.map((tire) => {
      const clientCost = calculateClientCost(tire.cost);
      return {
        name: tire.name,
        single: clientCost,
        two: (clientCost * 2).toFixed(2),
        three: (clientCost * 3).toFixed(2),
        four: (clientCost * 4).toFixed(2),
      };
    });
  };

  const estimate = generateEstimate();

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className={`container mx-auto p-6 bg-white rounded-lg shadow-md ${styles.printable}`}>
      <h1 className="text-3xl font-bold mb-6 text-center">Tire Pricing Estimator</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border-collapse">
          <thead>
            <tr>
              <th className="px-4 py-2 border">Tire Name</th>
              <th className="px-4 py-2 border">1 Tire</th>
              <th className="px-4 py-2 border">2 Tires</th>
              <th className="px-4 py-2 border">3 Tires</th>
              <th className="px-4 py-2 border">4 Tires</th>
              <th className="px-4 py-2 border not-printable">Actions</th>
            </tr>
          </thead>
          <tbody>
            {estimate.map((tire, index) => (
              <tr key={index}>
                <td className="px-4 py-2 border">{tire.name}</td>
                <td className="px-4 py-2 border">${tire.single}</td>
                <td className="px-4 py-2 border">${tire.two}</td>
                <td className="px-4 py-2 border">${tire.three}</td>
                <td className="px-4 py-2 border">${tire.four}</td>
                <td className="px-4 py-2 border not-printable">
                  <button
                    className="p-2 bg-red-500 text-white rounded shadow hover:bg-red-600 transition"
                    onClick={() => removeTire(index)}
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <p className="mt-4 text-center text-sm text-gray-700">
        Note: Buying 4 tires includes bonus servicing.
      </p>
    </div>
  );
};

export default TireEstimator;
