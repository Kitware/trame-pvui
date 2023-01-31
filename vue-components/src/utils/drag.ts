// Modified from https://www.w3schools.com/howto/howto_js_draggable.asp

import clamp from './clamp';

export function makeDraggable(
  element: HTMLElement,
  callback: () => void,
  bounds = {
    x: [],
    y: [],
  },
  snapPoints = {
    x: [],
    y: [],
  }
) {
  let pos1 = 0,
    pos2 = 0,
    pos3 = 0,
    pos4 = 0;

  function dragMouseDown(e: MouseEvent) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e: MouseEvent) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    let newX = element.offsetLeft - pos1;
    let newY = element.offsetTop - pos2;
    if (bounds.y.length == 2 && newY >= bounds.y[0] && newY <= bounds.y[1]) {
      element.style.top = newY + 'px';
      snapPoints.y.forEach((snap) => {
        if (Math.abs(snap - newY) <= 5) newY = snap;
      });
    }
    if (bounds.x.length == 2 && newX >= bounds.x[0] && newX <= bounds.x[1]) {
      snapPoints.x.forEach((snap) => {
        if (Math.abs(snap - newX) <= 5) newX = snap;
      });
      element.style.left = newX + 'px';
    }
    callback();
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }

  element.onmousedown = dragMouseDown;
}

export function listenDragSelection(
  element: HTMLElement,
  callback: (startPos: number, endPos: number) => void
) {
  let mousedownLocation: number | undefined = undefined;
  function dragMouseDown(e: MouseEvent) {
    if (
      e.target &&
      !(e.target as HTMLElement).classList.contains('color-square')
    ) {
      mousedownLocation = e.offsetX;
    }
  }

  function dragMouseUp(e: MouseEvent) {
    if (mousedownLocation !== undefined) {
      const lower = Math.min(mousedownLocation, e.offsetX);
      const upper = Math.max(mousedownLocation, e.offsetX);
      if (lower != upper) {
        callback(lower, upper);
      }
    }
  }

  element.onmousedown = dragMouseDown;
  element.onmouseup = dragMouseUp;
}

export function makeDraggableSVG(
  svg: SVGGraphicsElement,
  validateDrag: CallableFunction,
  callback: CallableFunction
) {
  let selectedShape: HTMLElement | undefined = undefined;
  let posOffset: Record<string, number> | undefined = undefined;
  svg.addEventListener('mousedown', startDrag as EventListener);
  window.addEventListener('mousemove', drag as EventListener);
  window.addEventListener('mouseup', endDrag as EventListener);
  const xRange = [40, svg.clientWidth - 40];

  function getMousePosition(evt: MouseEvent) {
    if (!svg) return { x: 0, y: 0 };
    const CTM = svg.getScreenCTM();
    if (!CTM) return { x: 0, y: 0 };
    return {
      x: (evt.clientX - CTM.e) / CTM.a,
      y: (evt.clientY - CTM.f) / CTM.d,
    };
  }

  function startDrag(evt: MouseEvent) {
    const target = evt.target as HTMLElement;
    if (target && target.classList.contains('draggable')) {
      selectedShape = target;
      posOffset = getMousePosition(evt);
      posOffset.x -= parseFloat(
        selectedShape.getAttributeNS(null, 'cx') || '0'
      );
      posOffset.y -= parseFloat(
        selectedShape.getAttributeNS(null, 'cy') || '0'
      );
    }
  }
  function drag(evt: MouseEvent) {
    if (selectedShape) {
      evt.preventDefault();
      const coord = getMousePosition(evt);
      if (posOffset) {
        coord.x -= posOffset.x;
        coord.y -= posOffset.y;
      }
      coord.x = clamp(coord.x, xRange[0], xRange[1]);
      const [moveX, moveY] = validateDrag(selectedShape, coord);
      if (!moveX) {
        coord.x = parseFloat(selectedShape.getAttributeNS(null, 'cx') || '0');
      }
      if (!moveY) {
        coord.y = parseFloat(selectedShape.getAttributeNS(null, 'cy') || '0');
      }

      selectedShape.setAttributeNS(null, 'cx', `${coord.x}`);
      selectedShape.setAttributeNS(null, 'cy', `${coord.y}`);
      callback(selectedShape, coord);
    }
  }
  function endDrag() {
    selectedShape = undefined;
  }
}
