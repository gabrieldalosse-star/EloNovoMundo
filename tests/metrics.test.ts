import assert from 'node:assert/strict';
import {percent,gauge,counter} from '../functions/src/metrics-utils.ts';
assert.equal(percent(null,1024),null);assert.equal(percent(100,0),null);assert.equal(percent(120,100),120);assert.equal(percent(256,1024),25);assert.equal(gauge([]).value,null);assert.equal(counter([]).value,null);
const sample={points:[{value:{int64Value:'256'},interval:{endTime:{seconds:1700000000}}}]};assert.equal(gauge([sample]).value,256);assert.equal(gauge([sample,sample]).value,null);assert.equal(counter([sample,sample]).value,512);console.log('Métricas: ausência, escopo ambíguo, percentuais, bytes e contadores verificados.');
