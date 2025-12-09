import React from 'react';


export default function EmptyState({ 
  icon: Icon, 
  title, 
  description, 
  actionLabel, 
  onAction,
  className = ""
}) {
  return (
    <div className={`flex flex-col items-center justify-center text-center p-8 md:p-12 bg-white rounded-xl border border-dashed border-slate-200 ${className}`}>
      {/* Icon Circle */}
      <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4 transition-transform hover:scale-110 duration-500">
        {Icon && <Icon size={32} className="text-slate-400" />}
      </div>
      
      {/* Text Content */}
      <h3 className="text-lg font-bold text-slate-800 mb-2">
        {title}
      </h3>
      
      <p className="text-slate-500 max-w-sm mb-6 text-sm leading-relaxed">
        {description}
      </p>
      
      {/* Optional Action Button */}
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="px-6 py-2 bg-blue-50 text-blue-600 font-bold text-sm rounded-lg hover:bg-blue-100 transition-colors active:scale-95"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
