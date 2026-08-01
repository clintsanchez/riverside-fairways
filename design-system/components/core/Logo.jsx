import React from 'react';

const files={
  primary:'logo-primary.png',
  reversed:'logo-reversed.png',
  ivory:'logo-ivory.png',
  mono:'logo-mono-black.png',
  icon:'icon-flag.png',
  'icon-reversed':'icon-flag-reversed.png'
};

export function Logo({variant='primary',height=64,basePath='assets',style,...rest}){
  return <img src={basePath+'/'+files[variant]} alt="Riverside Fairways" style={{height,width:'auto',display:'block',...style}} {...rest} />;
}
