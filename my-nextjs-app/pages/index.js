import React, { useState, useEffect } from 'react';
import NavBar from '../src/components/NavBar';
import PinInput from '../src/components/PinInput';
import Sidebar from '../src/components/Sidebar';
import TireEstimator from '../src/components/TireEstimator';
import { TireProvider } from '../src/context/TireContext';
import { TireBrandsProvider } from '../src/context/TireBrandsContext';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const accessGranted = localStorage.getItem('accessGranted');
    const accessExpiry = localStorage.getItem('accessExpiry');
    if (accessGranted && accessExpiry && new Date().getTime() < accessExpiry) {
      setIsAuthenticated(true);
    } else {
      localStorage.removeItem('accessGranted');
      localStorage.removeItem('accessExpiry');
    }
  }, []);

  const handleSuccess = () => {
    setIsAuthenticated(true);
  };

  if (!isAuthenticated) {
    return <PinInput onSuccess={handleSuccess} />;
  }

  return (
    <TireBrandsProvider>
      <TireProvider>
        <main className="flex min-h-screen">
          <div className="w-1/4 bg-gray-200">
            <Sidebar />
          </div>
          <div className="w-3/4 p-4 bg-gray-100">
            <NavBar />
            <TireEstimator />
          </div>
        </main>
      </TireProvider>
    </TireBrandsProvider>
  );
}
