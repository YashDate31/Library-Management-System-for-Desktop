import { useState, useEffect } from 'react';
import { X, Send, Loader2 } from 'lucide-react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

export default function RequestModal({ isOpen, onClose, type, defaultDetails = '', title }) {
  const [details, setDetails] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      setDetails(defaultDetails);
      setSuccess(false);
      setError('');
    }
  }, [isOpen, defaultDetails]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await axios.post('/api/request', {
        type: type,
        details: details
      });
      if (res.data.status === 'success') {
        setSuccess(true);
        setTimeout(() => {
          onClose();
        }, 2000);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit request');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="bg-surface border border-border rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transition-colors"
        >
          {/* Header */}
          <div className="p-4 border-b border-border flex justify-between items-center bg-background/50">
            <h3 className="font-bold text-text-primary">{success ? 'Request Sent!' : title}</h3>
            <button onClick={onClose} className="p-1 hover:bg-background rounded-full transition text-text-secondary hover:text-text-primary">
              <X size={20} />
            </button>
          </div>

          {/* Body */}
          <div className="p-6">
            {success ? (
              <div className="text-center py-6">
                <div className="w-16 h-16 bg-success/20 text-success rounded-full flex items-center justify-center mx-auto mb-4">
                  <Send size={32} />
                </div>
                <p className="text-text-secondary">Your request has been submitted successfully to the librarian.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit}>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-text-secondary mb-2">
                    Additional Details
                  </label>
                  <textarea
                    className="w-full p-3 rounded-xl bg-background border border-border text-text-primary focus:ring-2 focus:ring-primary/50 focus:border-primary outline-none min-h-[120px] resize-none text-sm placeholder:text-text-secondary transition-colors"
                    placeholder="Describe your request..."
                    value={details}
                    onChange={(e) => setDetails(e.target.value)}
                    required
                  />
                </div>
                
                {error && <p className="text-danger text-sm mb-4">{error}</p>}

                <div className="flex justify-end gap-3">
                  <button 
                    type="button" 
                    onClick={onClose}
                    className="px-4 py-2 text-text-secondary font-medium hover:bg-background hover:text-text-primary rounded-lg transition"
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    disabled={loading}
                    className="px-4 py-2 bg-primary text-white font-medium rounded-lg hover:bg-blue-600 transition flex items-center gap-2 disabled:opacity-70 shadow-lg shadow-primary/25"
                  >
                    {loading && <Loader2 size={16} className="animate-spin" />}
                    Submit Request
                  </button>
                </div>
              </form>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
