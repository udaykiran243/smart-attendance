import { QRCodeCanvas } from "qrcode.react";
import PropTypes from 'prop-types';

export default function RotatingQR({ token, onClose, compact = false }) {
  // If token is not provided (legacy usage), we might show loading or error
  // But for now assumes token is passed from parent
  
  return (
    <div className={`flex flex-col items-center gap-4 ${compact ? 'p-0' : 'p-4'}`}>
      <div className="transition-opacity duration-300">
        <QRCodeCanvas value={token || "loading..."} size={compact ? 200 : 250} />
      </div>
      
      {!compact && (
        <button
          onClick={onClose}
          className="mt-2 px-4 py-2 bg-[var(--danger)] text-[var(--text-on-primary)] rounded cursor-pointer hover:opacity-90 transition"
        >
          Stop Session
        </button>
      )}
    </div>
  );
}

RotatingQR.propTypes = {
  token: PropTypes.string,
  onClose: PropTypes.func.isRequired,
  compact: PropTypes.bool,
};
