// Observation-only Frida template. Replace TARGET with an authorized target method.
Java.perform(function () {
  const Target = Java.use('TARGET');
  const overload = Target.METHOD.overload();
  overload.implementation = function () {
    console.log('[enter] TARGET.METHOD');
    const result = overload.apply(this, arguments);
    console.log('[return] ' + result);
    return result;
  };
});
