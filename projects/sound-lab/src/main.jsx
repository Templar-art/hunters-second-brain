import ReactDOM from 'react-dom/client';
import ChakraScope from './components/setup/ChakraScope';
import SoundLab from './tools/sound-lab/SoundLab';
import { initInputModeTracking } from './utils/inputMode';
import './app.css';

initInputModeTracking();

ReactDOM.createRoot(document.getElementById('root')).render(
  <ChakraScope>
    <div className="tool-shell">
      <SoundLab />
    </div>
  </ChakraScope>
);
