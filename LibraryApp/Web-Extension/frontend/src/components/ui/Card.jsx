import React from 'react';
import PropTypes from 'prop-types';

const Card = ({ children, className = '', noPadding = false, ...props }) => {
  return (
    <div 
      className={`card ${noPadding ? 'p-0' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

Card.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
  noPadding: PropTypes.bool,
};

export default Card;
