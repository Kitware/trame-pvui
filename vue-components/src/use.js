import components from './components';
import icons from './icons';
import simputWidgets from './simput';

const VUE_COMPONENTS = [components, icons, simputWidgets];

export function install(Vue) {
  VUE_COMPONENTS.forEach((components) => {
    Object.keys(components).forEach((name) => {
      Vue.component(name, components[name]);
    });
  });
}
