const base=import.meta.env.BASE_URL;
export const brandAsset=(name:string)=>`${base}brand/${name}`;
export function Brand({light=false,className=''}:{light?:boolean,className?:string}){return <img className={`elo-wordmark ${className}`} src={brandAsset(light?'elo-horizontal-claro.svg':'elo-horizontal.svg')} width="300" height="114" alt="ELO Novo Mundo"/>}
export function SchoolSeal(){return <span className="school-seal"><img src={brandAsset('colegio-novo-mundo-original.png')} alt="Colégio Novo Mundo — logo do site institucional"/></span>}
