(() => {
  const originalFetch = window.fetch;
  window.fetch = async function (...args) {
    console.log('[fetch:request]', args[0], args[1] || {});
    const response = await originalFetch.apply(this, args);
    console.log('[fetch:response]', response.status, response.url);
    return response;
  };
})();
