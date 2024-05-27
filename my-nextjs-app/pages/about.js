"use client";

import NavBar from '../src/components/NavBar';

const About = () => {
  return (
    <div>
      <NavBar />
      <main className="flex flex-col items-center justify-center min-h-screen p-24">
        <h1 className="text-4xl font-bold mb-8">About Us</h1>
        <p className="mb-4 max-w-2xl text-center">
          Welcome to Ocean Heights Auto and Tire! Located in the heart of Egg Harbor Township, New Jersey,
          we have been providing top-notch automotive services to our community for several years. Our team
          of experienced technicians is dedicated to ensuring your vehicle is safe and running smoothly.
        </p>
        <p className="mb-4 max-w-2xl text-center">
          At Ocean Heights Auto and Tire, we offer a wide range of services including tire sales and installation,
          brake repair, oil changes, engine diagnostics, and general vehicle maintenance. We pride ourselves on
          delivering exceptional customer service and quality workmanship at affordable prices.
        </p>
        <p className="mb-4 max-w-2xl text-center">
          Our mission is to provide reliable and trustworthy automotive care to our customers. We understand
          the importance of having a dependable vehicle, and we are here to help you keep it in the best
          condition possible. Thank you for choosing Ocean Heights Auto and Tire for all your automotive needs.
        </p>
      </main>
    </div>
  );
};

export default About;
