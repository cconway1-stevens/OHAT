import '../src/styles/globals.css';
import '../src/styles/Print.module.css';
import { TireBrandsProvider } from '../src/context/TireBrandsContext';
import { TireProvider } from '../src/context/TireContext';

function MyApp({ Component, pageProps }) {
  return (
    <TireBrandsProvider>
      <TireProvider>
        <Component {...pageProps} />
      </TireProvider>
    </TireBrandsProvider>
  );
}

export default MyApp;
