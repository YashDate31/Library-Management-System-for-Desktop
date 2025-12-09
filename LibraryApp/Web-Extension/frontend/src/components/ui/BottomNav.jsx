import React from 'react';
import PropTypes from 'prop-types';
import { NavLink } from 'react-router-dom';

const BottomNav = ({ items = [] }) => {
  return (
    <nav className="fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-slate-100 flex justify-around items-center pb-safe z-50 md:hidden shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
      {items.map((item) => (
        <NavLink
          key={item.label}
          to={item.to}
          className={({ isActive }) => `
            flex flex-col items-center justify-center w-full h-full gap-1
            transition-colors duration-200
            ${isActive ? 'text-blue-600' : 'text-slate-400 hover:text-slate-600'}
          `}
        >
          {({ isActive }) => (
            <>
              <div className={`transition-transform duration-200 ${isActive ? '-translate-y-0.5' : ''}`}>
                {isActive ? item.activeIcon || item.icon : item.icon}
              </div>
              <span className="text-[10px] font-medium leading-none">{item.label}</span>
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
};

BottomNav.propTypes = {
  items: PropTypes.arrayOf(PropTypes.shape({
    label: PropTypes.string.isRequired,
    to: PropTypes.string.isRequired,
    icon: PropTypes.element.isRequired,
    activeIcon: PropTypes.element,
  })).isRequired,
};

export default BottomNav;
