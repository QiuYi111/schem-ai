/**
 * Schematic Viewer - A lightweight, premium web renderer for schem-ai
 */

class SchematicViewer {
    constructor(containerId, data) {
        this.container = document.getElementById(containerId);
        this.data = data;
        this.svg = null;
        this.g = null;
        this.zoom = 1;
        this.offset = { x: 0, y: 0 };
        this.init();
    }

    init() {
        this.container.innerHTML = '';
        this.container.style.backgroundColor = '#1a1a1a';
        this.container.style.color = '#e0e0e0';
        this.container.style.fontFamily = "'Inter', sans-serif";
        this.container.style.overflow = 'hidden';
        this.container.style.position = 'relative';

        this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        this.svg.setAttribute("width", "100%");
        this.svg.setAttribute("height", "100%");
        this.svg.style.cursor = "grab";
        this.container.appendChild(this.svg);

        this.g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        this.svg.appendChild(this.g);

        this.render();
        this.setupInteractions();
    }

    render() {
        const { components, modules, nets } = this.data;
        
        let currentX = 100;
        let currentY = 100;
        const spacing = 300;

        // Render Components
        components.forEach((comp, index) => {
            this.renderComponent(comp, currentX, currentY);
            currentX += spacing;
            if (currentX > 1000) {
                currentX = 100;
                currentY += spacing * 1.5;
            }
        });
    }

    renderComponent(comp, x, y) {
        const width = 180;
        const padding = 20;
        const pinHeight = 25;
        const pins = comp.pins || [];
        const height = Math.max(80, pins.length * pinHeight + padding * 2);

        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        group.setAttribute("transform", `translate(${x}, ${y})`);
        this.g.appendChild(group);

        // Component Body
        const body = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        body.setAttribute("width", width);
        body.setAttribute("height", height);
        body.setAttribute("rx", "4");
        body.setAttribute("fill", "#2d2d2d");
        body.setAttribute("stroke", "#4a4a4a");
        body.setAttribute("stroke-width", "2");
        group.appendChild(body);

        // Component Name
        const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
        title.setAttribute("x", width / 2);
        title.setAttribute("y", -10);
        title.setAttribute("text-anchor", "middle");
        title.setAttribute("fill", "#00d4ff");
        title.setAttribute("font-weight", "600");
        title.textContent = comp.name;
        group.appendChild(title);

        const ref = document.createElementNS("http://www.w3.org/2000/svg", "text");
        ref.setAttribute("x", width / 2);
        ref.setAttribute("y", -28);
        ref.setAttribute("text-anchor", "middle");
        ref.setAttribute("fill", "#888");
        ref.setAttribute("font-size", "12");
        ref.textContent = comp.ref || "U?";
        group.appendChild(ref);

        // Pins
        pins.forEach((pin, i) => {
            const pinY = padding + i * pinHeight + pinHeight / 2;
            
            // Pin Line
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", -15);
            line.setAttribute("y1", pinY);
            line.setAttribute("x2", 0);
            line.setAttribute("y2", pinY);
            line.setAttribute("stroke", "#666");
            group.appendChild(line);

            // Pin Label (Inside)
            const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
            label.setAttribute("x", 8);
            label.setAttribute("y", pinY + 4);
            label.setAttribute("fill", "#bbb");
            label.setAttribute("font-size", "11");
            label.textContent = pin.name;
            group.appendChild(label);

            // Net Label (Outside - THE GATING REQUIREMENT)
            if (pin.net) {
                const netLabelGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
                netLabelGroup.setAttribute("class", "net-label");
                netLabelGroup.style.cursor = "pointer";
                
                const netRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                const netText = document.createElementNS("http://www.w3.org/2000/svg", "text");
                netText.textContent = pin.net;
                netText.setAttribute("x", -25);
                netText.setAttribute("y", pinY + 4);
                netText.setAttribute("text-anchor", "end");
                netText.setAttribute("fill", "#ff9f43");
                netText.setAttribute("font-size", "11");
                netText.setAttribute("font-family", "monospace");
                
                netLabelGroup.appendChild(netText);
                group.appendChild(netLabelGroup);

                // Highlight interactions
                netLabelGroup.addEventListener('mouseenter', () => this.highlightNet(pin.net));
                netLabelGroup.addEventListener('mouseleave', () => this.clearHighlight());
            }
        });
    }

    highlightNet(netName) {
        const labels = this.g.querySelectorAll('.net-label');
        labels.forEach(l => {
            const text = l.querySelector('text');
            if (text.textContent === netName) {
                text.setAttribute('fill', '#fff');
                text.setAttribute('font-weight', 'bold');
                text.style.filter = 'drop-shadow(0 0 5px #ff9f43)';
            } else {
                l.style.opacity = '0.3';
            }
        });
    }

    clearHighlight() {
        const labels = this.g.querySelectorAll('.net-label');
        labels.forEach(l => {
            const text = l.querySelector('text');
            text.setAttribute('fill', '#ff9f43');
            text.setAttribute('font-weight', 'normal');
            text.style.filter = 'none';
            l.style.opacity = '1';
        });
    }

    setupInteractions() {
        let isDragging = false;
        let startPos = { x: 0, y: 0 };

        this.svg.addEventListener('mousedown', (e) => {
            isDragging = true;
            this.svg.style.cursor = "grabbing";
            startPos = { x: e.clientX - this.offset.x, y: e.clientY - this.offset.y };
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            this.offset.x = e.clientX - startPos.x;
            this.offset.y = e.clientY - startPos.y;
            this.updateTransform();
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
            this.svg.style.cursor = "grab";
        });

        this.svg.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            this.zoom *= delta;
            this.zoom = Math.min(Math.max(0.1, this.zoom), 5);
            this.updateTransform();
        });
    }

    updateTransform() {
        this.g.setAttribute("transform", `translate(${this.offset.x}, ${this.offset.y}) scale(${this.zoom})`);
    }
}
