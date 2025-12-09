import { useState } from 'react';
import { X, AlertTriangle } from 'lucide-react';
import axios from 'axios';
import Button from './ui/Button';

export default function DangerValidationModal({ isOpen, onClose, user, onSuccess }) {
  const [step, setStep] = useState(1); // 1: Warning, 2: Typing, 3: Password
  const [confirmationText, setConfirmationText] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const confirmationString = `delete ${user?.enrollment_no}`;
  
  const handleFinalSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const { data } = await axios.post('/api/request-deletion', { 
        password,
        reason: 'User requested via Danger Modal'
      });
      if (data.status === 'success') {
         onSuccess();
         onClose();
      } else {
         setError(data.message);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative w-full max-w-lg bg-white rounded-xl shadow-2xl border border-red-200 overflow-hidden animate-fade-in">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 bg-slate-50 border-b border-slate-100">
          <h3 className="font-bold text-slate-800">
             Delete Account Request
          </h3>
          <button onClick={onClose} className="p-1 hover:bg-slate-200 rounded-full transition-colors">
            <X size={20} className="text-slate-500" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
            
          {/* Warning Banner */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <div className="flex gap-3">
              <AlertTriangle className="text-yellow-600 shrink-0" size={20} />
              <div>
                <h4 className="font-bold text-yellow-800 text-sm mb-1">Unexpected bad things will happen if you don't read this!</h4>
                <ul className="list-disc list-inside text-xs text-yellow-700 space-y-1">
                  <li>This will permanently disable your access to the library portal.</li>
                  <li>This request will be sent to the <strong>Librarian</strong> for final approval.</li>
                  <li>Once approved by the librarian, all your data including borrowing history will be wiped.</li>
                </ul>
              </div>
            </div>
          </div>

          {step === 1 && (
             <div className="space-y-4">
               <p className="text-sm text-slate-600">
                 Please confirm that you want to initiate the deletion request for account <strong>{user?.enrollment_no}</strong>.
               </p>
               <Button 
                 variant="ghost" 
                 onClick={() => setStep(2)}
                 className="w-full border border-slate-300 hover:bg-slate-50 text-slate-700"
               >
                 I have read and understand these effects
               </Button>
             </div>
          )}

          {step === 2 && (
            <div className="space-y-4 animate-fade-in">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">
                  To confirm, type "<span className="font-mono font-bold select-all">{confirmationString}</span>" in the box below
                </label>
                <input 
                  type="text"
                  value={confirmationText}
                  onChange={(e) => setConfirmationText(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 outline-none font-mono text-sm"
                  autoFocus
                />
              </div>
              <Button 
                variant="danger" 
                onClick={() => setStep(3)}
                disabled={confirmationText !== confirmationString}
                className="w-full"
              >
                Delete this account
              </Button>
            </div>
          )}

          {step === 3 && (
             <div className="space-y-4 animate-fade-in">
               <div className="text-center mb-4">
                 <p className="text-sm text-slate-500">Confirm access</p>
                 <div className="font-mono bg-slate-100 inline-block px-2 py-1 rounded text-xs mt-1 border border-slate-200">
                   Signed in as <strong>{user?.enrollment_no}</strong>
                 </div>
               </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-slate-700">
                    Password
                  </label>
                  <input 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    autoFocus
                  />
                  {error && <p className="text-xs text-red-600 font-medium">{error}</p>}
                </div>

                <div className="pt-2">
                  <Button 
                    variant="primary" 
                    onClick={handleFinalSubmit}
                    isLoading={loading}
                    className="w-full bg-green-600 hover:bg-green-700 border-transparent"
                  >
                    Verify
                  </Button>
                </div>
             </div>
          )}

        </div>
      </div>
    </div>
  );
}
