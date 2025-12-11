import { useState, useEffect } from 'react';
import axios from 'axios';
import DangerValidationModal from '../components/DangerValidationModal';
import { motion, AnimatePresence } from 'framer-motion';
import { Settings as SettingsIcon, Bell, Shield, Moon, Trash2, Key, Mail, Save, X, Loader2 } from 'lucide-react';

export default function Settings({ user, setUser }) {
  // Local state for settings form
  const [email, setEmail] = useState('');
  const [libraryAlerts, setLibraryAlerts] = useState(false);
  const [loanReminders, setLoanReminders] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  const [dataConsent, setDataConsent] = useState(true);

  // Initialize state from user prop when available
  useEffect(() => {
    if (user) {
        setEmail(user.email || '');
        // Use user.settings if available, or fallbacks
        const settings = user.settings || {};
        setLibraryAlerts(settings.libraryAlerts ?? false);
        setLoanReminders(settings.loanReminders ?? true);
        setDarkMode(settings.theme === 'dark');

        setDataConsent(settings.dataConsent ?? true);
    }
  }, [user]);

  // Password Change State
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isSavingPassword, setIsSavingPassword] = useState(false);
  const [passwordMsg, setPasswordMsg] = useState('');
  
  // General Save State
  const [isSaving, setIsSaving] = useState(false);

  // Deletion Modal State
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  // Initial State for dirty checking (Derived from user prop to keep in sync)
  const initialSettings = {
    email: user?.email || '',
    libraryAlerts: user?.settings?.libraryAlerts ?? false,
    loanReminders: user?.settings?.loanReminders ?? true,
    darkMode: user?.settings?.theme === 'dark',

    dataConsent: user?.settings?.dataConsent ?? true
  };

  const isDirty = 
    email !== initialSettings.email ||
    libraryAlerts !== initialSettings.libraryAlerts ||
    loanReminders !== initialSettings.loanReminders ||
    darkMode !== initialSettings.darkMode ||

    dataConsent !== initialSettings.dataConsent;

  const handleChangePassword = async () => {
    if (newPassword.length < 4) {
        setPasswordMsg('Password must be at least 4 characters');
        return;
    }
    if (newPassword !== confirmPassword) {
        setPasswordMsg('Passwords do not match');
        return;
    }

    setIsSavingPassword(true);
    setPasswordMsg('');

    try {
        const { data } = await axios.post('/api/change_password', { new_password: newPassword });
        if (data.status === 'success') {
            setPasswordMsg('Success! Password updated.');
            setTimeout(() => window.location.reload(), 1000);
        } else {
            setPasswordMsg(data.message || 'Failed to update');
        }
    } catch (e) {
        setPasswordMsg(e.response?.data?.message || 'Server error');
    } finally {
        setIsSavingPassword(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
        const payload = {
            email,
            libraryAlerts,
            loanReminders,
            theme: darkMode ? 'dark' : 'light',

            dataConsent
        };

        const { data } = await axios.post('/api/settings', payload);
        
        if (data.status === 'success') {
            // Optimistic update of parent state if possible, or force reload
            // Ideally notify user and update 'user' prop context
            alert("Settings saved successfully!");
            
            // Trigger a silent reload of user data if possible, or just reload page
            window.location.reload(); 
        } else {
           alert(data.message || "Failed to save settings.");
        }
    } catch (e) {
        console.error(e);
        alert("Failed to save settings. Please try again.");
    } finally {
        setIsSaving(false);
    }
  };

  const resetChanges = () => {
    setEmail(initialSettings.email);
    setLibraryAlerts(initialSettings.libraryAlerts);
    setLoanReminders(initialSettings.loanReminders);
    setDarkMode(initialSettings.darkMode);

    setDataConsent(initialSettings.dataConsent);
  };



  return (
    <div className="max-w-5xl mx-auto px-4 pb-32 font-sans relative">
      
      {/* Header */}
      <div className="mb-10 text-center">
        <motion.div 
            initial={{ scale: 0.9, opacity: 0 }} 
            animate={{ scale: 1, opacity: 1 }}
            className="inline-flex items-center justify-center p-3 bg-white rounded-2xl shadow-md mb-4"
        >
            <SettingsIcon className="text-slate-700" size={32} />
        </motion.div>
        <h1 className="text-4xl font-black text-slate-900 tracking-tight mb-2">Settings</h1>
        <p className="text-slate-500 font-medium">Customize your student portal experience.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Account Panel */}
        <Panel title="Account" icon={Shield} delay={0.1}>
             {/* Email */}
             <div className="space-y-2">
                <label className="text-sm font-bold text-slate-700 dark:text-slate-300 flex items-center gap-2 transition-colors">
                    <Mail size={16} /> Email Address
                </label>
                <input 
                  type="email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:bg-white dark:focus:bg-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all font-medium text-slate-800 dark:text-white"
                />
             </div>

             {/* Password Accordion */}
             <div className="bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-700 overflow-hidden transition-all">
                {!isChangingPassword ? (
                    <button 
                         onClick={() => setIsChangingPassword(true)}
                         className="w-full flex items-center justify-between p-4 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-left"
                    >
                        <span className="font-bold text-slate-700 dark:text-slate-300 flex items-center gap-2">
                            <Key size={18} className="text-slate-400" /> Change Password
                        </span>
                        <span className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 px-3 py-1 rounded-lg text-xs font-bold text-slate-500 dark:text-slate-400 shadow-sm transition-colors">Edit</span>
                    </button>
                ) : (
                    <div className="p-4 space-y-4 animate-in slide-in-from-top-2">
                         <div className="flex items-center justify-between mb-2">
                             <span className="font-bold text-slate-900 dark:text-white text-sm">Update Password</span>
                             <button onClick={() => setIsChangingPassword(false)} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                                 <X size={16} />
                             </button>
                         </div>
                         <input 
                             type="password"
                             value={newPassword}
                             onChange={(e) => setNewPassword(e.target.value)}
                             className="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm text-slate-900 dark:text-white transition-colors"
                             placeholder="New password (min 4 chars)"
                         />
                         <input 
                             type="password"
                             value={confirmPassword}
                             onChange={(e) => setConfirmPassword(e.target.value)}
                             className="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm text-slate-900 dark:text-white transition-colors"
                             placeholder="Confirm new password"
                         />
                         
                         <div className="flex items-center justify-between pt-2">
                             <span className={`text-xs font-bold ${passwordMsg.includes('Success') ? 'text-green-600 dark:text-green-400' : 'text-red-500 dark:text-red-400'}`}>
                                 {passwordMsg}
                             </span>
                             <button 
                                 onClick={handleChangePassword}
                                 disabled={isSavingPassword}
                                 className="px-4 py-2 bg-slate-900 dark:bg-blue-600 text-white text-xs font-bold rounded-lg hover:bg-slate-800 dark:hover:bg-blue-500 transition-colors"
                             >
                                 {isSavingPassword ? 'Saving...' : 'Update'}
                             </button>
                         </div>
                    </div>
                )}
             </div>
        </Panel>

        {/* Preferences Panel */}
        <div className="space-y-8">
            <Panel title="Preferences" icon={Moon} delay={0.2}>
                <div className="flex items-center justify-between group">
                    <div>
                        <span className="block font-bold text-slate-800 dark:text-white text-lg transition-colors">Dark Mode</span>
                        <span className="text-xs font-medium text-slate-400 dark:text-slate-500 group-hover:text-slate-500 dark:group-hover:text-slate-400 transition-colors">Reduce eye strain at night</span>
                    </div>
                    <Switch checked={darkMode} onChange={(checked) => {
                        setDarkMode(checked);
                        if (checked) {
                            document.documentElement.classList.add('dark');
                            localStorage.setItem('theme', 'dark');
                        } else {
                            document.documentElement.classList.remove('dark');
                            localStorage.setItem('theme', 'light');
                        }
                    }} />
                </div>


            </Panel>

            <Panel title="Notifications" icon={Bell} delay={0.3}>
                <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-700 dark:text-slate-300 transition-colors">Library Alerts</span>
                    <Switch checked={libraryAlerts} onChange={setLibraryAlerts} />
                </div>
                <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-700 dark:text-slate-300 transition-colors">Loan Reminders</span>
                    <Switch checked={loanReminders} onChange={setLoanReminders} />
                </div>
            </Panel>
        </div>

        {/* Danger Zone */}
        <div className="lg:col-span-2">
             <motion.div 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="bg-red-50/50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/30 rounded-3xl p-6 flex flex-col md:flex-row items-center justify-between gap-6 transition-colors"
             >
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-2xl transition-colors">
                        <Trash2 size={24} />
                    </div>
                    <div>
                        <h3 className="font-bold text-red-900 dark:text-red-400 text-lg transition-colors">Delete Account</h3>
                        <p className="text-red-700/80 dark:text-red-300/60 text-sm font-medium transition-colors">Permanently remove your data from the system.</p>
                    </div>
                </div>
                <button 
                  onClick={() => setIsDeleteModalOpen(true)}
                  className="px-6 py-3 bg-white dark:bg-slate-800 border border-red-200 dark:border-red-900/50 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 font-bold rounded-xl transition-colors shadow-sm"
                >
                  Request Deletion
                </button>
             </motion.div>
        </div>

      </div>

      {/* Floating Action Bar */}
      <AnimatePresence>
        {isDirty && (
            <motion.div 
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: 100, opacity: 0 }}
                className="fixed bottom-32 md:bottom-8 left-1/2 -translate-x-1/2 bg-slate-900/90 dark:bg-blue-600/90 text-white p-2 pl-6 pr-2 rounded-full shadow-2xl flex items-center gap-6 z-[100] border border-slate-700/50 dark:border-blue-500/50 backdrop-blur-md w-[calc(100%-2rem)] md:w-auto justify-between md:justify-start"
            >
                <span className="font-bold text-sm text-slate-200 whitespace-nowrap">Unsaved changes</span>
                <div className="flex items-center gap-2">
                    <button 
                        onClick={resetChanges}
                        className="px-4 py-2 hover:bg-slate-800 rounded-full text-sm font-bold transition-colors text-slate-400 hover:text-white"
                        disabled={isSaving}
                    >
                        Reset
                    </button>
                    <button 
                        onClick={handleSave}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-full text-sm font-bold shadow-lg shadow-blue-900/50 transition-all active:scale-95 flex items-center gap-2"
                        disabled={isSaving}
                    >
                        {isSaving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
                        {isSaving ? 'Saving...' : 'Save'}
                    </button>
                </div>
            </motion.div>
        )}
      </AnimatePresence>

      <DangerValidationModal 
        isOpen={isDeleteModalOpen} 
        onClose={() => setIsDeleteModalOpen(false)}
        user={user}
        onSuccess={() => alert("Deletion request sent.")}
      />
    </div>
  );
}



const Panel = ({ title, icon: Icon, children, delay }) => (
  <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="bg-white/80 dark:bg-slate-800/90 backdrop-blur-xl rounded-3xl border border-white/50 dark:border-slate-700/50 shadow-xl shadow-slate-200/50 dark:shadow-slate-900/50 p-6 md:p-8 relative overflow-hidden transition-colors"
  >
      <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
          <Icon size={120} className="dark:text-white" />
      </div>
      <div className="flex items-center gap-3 mb-8 relative z-10">
          <div className="p-3 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-2xl shadow-sm transition-colors">
              <Icon size={24} />
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white transition-colors">{title}</h2>
      </div>
      <div className="relative z-10 space-y-6">
          {children}
      </div>
  </motion.div>
);

// iOS Style Switch
function Switch({ checked, onChange }) {
  return (
    <button 
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`
        w-14 h-8 rounded-full relative transition-colors duration-300 ease-spring focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2
        ${checked ? 'bg-blue-600' : 'bg-slate-200 dark:bg-slate-700'}
      `}
    >
      <motion.div
        layout
        transition={{ type: "spring", stiffness: 700, damping: 30 }}
        className={`
          absolute top-1 left-1 bg-white rounded-full shadow-md w-6 h-6 pointer-events-none
        `}
        animate={{ x: checked ? 24 : 0 }}
      />
    </button>
  );
}
