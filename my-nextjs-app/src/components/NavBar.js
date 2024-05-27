import React from 'react';
import Link from 'next/link';

const NavBar = () => {
  return (
    <nav className="p-4 bg-blue-500 text-white">
      <ul className="flex space-x-4">
        <li>
          <Link href="/" legacyBehavior>
            <a>Home</a>
          </Link>
        </li>
        <li>
          <Link href="/manage-brands" legacyBehavior>
            <a>Manage Brands</a>
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
