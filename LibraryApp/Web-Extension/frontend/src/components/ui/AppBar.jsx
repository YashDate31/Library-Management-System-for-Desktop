import React from 'react';
import PropTypes from 'prop-types';

const AppBar = ({ title, rightAction, onBack, className = '' }) => {
  return (
    <header className={`sticky top-0 z-40 flex items-center justify-between px-4 h-16 bg-white/80 backdrop-blur-md border-b border-slate-100 transition-all ${className}`}>
      <div className="flex items-center gap-3">
        {onBack && (
          <button 
            onClick={onBack}
            className="p-2 -ml-2 rounded-full hover:bg-slate-100 text-slate-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6"/></svg>
          </button>
        )}
        <h1 className="text-lg font-heading font-semibold text-slate-900 tracking-tight">{title}</h1>
      </div>
      
      {rightAction && (
        <div className="flex items-center">
          {rightAction}
        </div>
      )}
    </header>
  );
};

AppBar.propTypes = {
  title: PropTypes.string.isRequired,
  rightAction: PropTypes.node,
  onBack: PropTypes.func,
  className: PropTypes.string,
};

export default AppBar;
