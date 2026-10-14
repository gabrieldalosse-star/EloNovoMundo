import {initial,reduceState} from '../functions/src/domain';
import {call,configured} from './firebase';
const key='elo-local-demo-v1';
function local(){const raw=localStorage.getItem(key);return raw?JSON.parse(raw):{revision:0,state:initial()}}
export async function readWorkspace(){if(configured)return call('pilotWorkspace',{operation:'read'});return local()}
export async function writeWorkspace(action:unknown,revision:number){if(configured)return call('pilotWorkspace',{operation:'write',action,revision});const current=local();if(current.revision!==revision)throw Error('Alterações em outra aba. Copie seu texto e recarregue os dados.');const value={state:reduceState(current.state,action),revision:revision+1};localStorage.setItem(key,JSON.stringify(value));return value}
