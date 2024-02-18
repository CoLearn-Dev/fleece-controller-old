import { Timeline, Tag } from "antd-v5";
import G6 from '@antv/g6';
import { Space, Input, Button, Card, } from 'antd';
import { CheckCircleOutlined, MessageOutlined } from '@ant-design/icons';
import { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';

const ChatBox: React.FC = () => {
    const lineDash = [4, 2, 1, 2];
    G6.registerEdge(
        'line-dash',
        {
          afterDraw(cfg, group) {
            // get the first shape in the group, it is the edge's path here=
            const shape = group.get('children')[0];
            let index = 0;
            // Define the animation
            shape.animate(
              () => {
                index++;
                if (index > 9) {
                  index = 0;
                }
                const res = {
                  lineDash,
                  lineDashOffset: -index,
                };
                // returns the modified configurations here, lineDash and lineDashOffset here
                return res;
              },
              {
                repeat: true, // whether executes the animation repeatly
                duration: 3000, // the duration for executing once
              },
            );
          },
        },
        'line', // extend the built-in edge 'cubic'
      );
      

    const ref = useRef(null);
    let graph = null;

    const data = {
        nodes: [
            {
                id: 'node A',
                label: 'node A',
                // the attributes for drawing donut
                donutAttrs: {
                    'used': 6,
                    'remained': 2,
                },
                start: true,
            },
            {
                id: 'node B',
                label: 'node B',
                donutAttrs: {
                    'used': 8,
                    'remained': 8,
                },
            },
            {
                id: 'node C',
                label: 'node C',
                donutAttrs: {
                    'used': 2,
                    'remained': 2,
                },
            },
        ],
        edges: [
            { source: 'node A', target: 'node B', latency: 120 },
            { source: 'node B', target: 'node C', latency: 30 },
            { source: 'node C', target: 'node A', latency: 60 },
        ]
    };

    data.edges.forEach(edge => {
        edge.label = `${edge.latency} ms`
        edge.size = Math.sqrt(5000 / edge.latency)
    })

    const colors = {
        'used': '#FDB515',
        'remained': '#65789B',
    }

    data.nodes.forEach(node => {
        node.donutColorMap = colors;
        node.size = 0;
        Object.keys(node.donutAttrs).forEach(key => {
            node.size += node.donutAttrs[key];
        });
        node.size = Math.sqrt(node.size) * 20;
        if (node.start) {
            node.icon = {
                show: true,
                height: 20,
                width: 20,
                img: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAYAAAA4qEECAAAACXBIWXMAAAsTAAALEwEAmpwYAAADMUlEQVR4nO2dPYtTQRSGR0RFBYvkDMvqlirWClr7A/wLNhY2fpS29rp+ISiWdsZGkjlxtVXXFUTttbGyWD+KVXDZcxiZFF4CSUzW3Jk7Z84DAyEJ5OThMHnv3GFijKIoiqIoSuPw/cN7yMElQlgjBz8HY/DYXgyvpa5PBL7XOkQIHxitHzUI4X14T+o68+/kCZKHZGtnb58wXfxLciXbXviPjyobQvtmatEOXqeuN1vIwcYMojdS15sthPbH9KLtt9T1ZgshrM7Q0S9S15st5NrnZxB9LnW92eLfml2E8GqKeLfmO2Z36nqzxj9pHwwiJ0he9U9hMXWdIgjdOk60dvKcGSd63PvDlSI7e5PQfieEr+zsA49wdN51mdJFs7O3Rlw9Mjt47B2ciFu9YNGhk3nSj6iD51uufTrut5DY0dNf6LwjtGd9x+yM+40KE81VDv9ECJeLXwWsWzRXcfELOXvFP1vYb0oklmiuhK8z2qt+5UDLlERs0VxNKWEF8bbvt5ZMCaQSzVU03GSEh77bPmYkk1o0V8KZne15t3DKSKQponl4Wnm51W+fMZJoomiWmMWbLJolZfEcRLOELJ6TaM45i+comnPM4jmL5pyyuATRnEMWlySam5zFpYrmpmVx6aK5KVm8FNGcOouXJppTZfFSRXPsLF66aP7b4XYz7FepbeOQirbD0p29rqIxRmfDuopGFe3lDLimHY01ThkOfrOzy2HvuIrGWgRrvOOaf/T0ggXrFGw/D9Y8uov7apkiSs/R5OCjLiphnYJ1mdTX3MG68M9138rqtU6apiFhjia9OWvrnh50uwHX2sG6gcaLzMClzNGUOgNLF01NycBSRVPTMrAk0dTkDCxBNOWQgXMWTTll4BxFU44ZOCfRlHMGzkE0ScjATRZNkjJwCtHhwEGeKBlW9GCUOYhmtDdGzL/MaB/5LhyfVwOY0kUPThZzdjkcXDXo7nB4VQ+OxK26ANHKNlHRkVDRkVDRkVDRkVDRkVDRkVDRkVDRCf9YIRz0Guvzi4Ed3B2xMHQndV3i8J2lvYz2PiH8CoMd3AvPpa5LLN6bHWGkrkNRFEVRFJMHfwCViPxnRKAsQgAAAABJRU5ErkJggg=="
            }
        }
    })

    const legendData = {
        nodes: [{
            id: 'used',
            label: 'Used memory',
            order: 0,
            style: {
                fill: '#FDB515',
            }
        }, {
            id: 'remained',
            label: 'Remaining memory',
            order: 1,
            style: {
                fill: '#65789B',
            },
        }]
    }
    
    const legend = new G6.Legend({
        data: legendData,
        align: 'center',
        layout: 'vertical',
        position: 'top-right',
        vertiSep: 8,
        horiSep: 8,
        offsetY: -4,
        padding: [8, 8, 8, 8],
        containerStyle: {
            fill: '#ccc',
            lineWidth: 2
        },
        title: ' ',
        titleConfig: {
            offsetY: -24,
        },
    });

    useEffect(() => {
        
        const width = ReactDOM.findDOMNode(ref.current).scrollWidth;
        const height = ReactDOM.findDOMNode(ref.current).scrollHeight || 300;
        if (!graph) {
            graph = new G6.Graph({
                container: ReactDOM.findDOMNode(ref.current),
                width: width,
                height: height,
                fitCenter: true,
                plugins: [legend],
                modes: {
                    default: ['drag-canvas', 'drag-node', 'zoom-canvas'],
                },
                layout: {
                    type: 'radial',
                    focusNode: 'li',
                    linkDistance: 200,
                    unitRadius: 200
                },
                defaultEdge: {
                    type: 'line-dash',
                    labelCfg: {
                        autoRotate: true,
                        style: {
                            stroke: "#fff",
                            lineWidth: 3
                        }
                    }
                },
                defaultNode: {
                    type: 'donut',
                    style: {
                        lineWidth: 0,
                    },
                    labelCfg: {
                        position: 'bottom',
                    },
                },
            });
        }
        graph.data(data);
        graph.render();

        graph.on('node:mouseenter', (evt) => {
            const { item } = evt;
            graph.setItemState(item, 'active', true);
        });

        graph.on('node:mouseleave', (evt) => {
            const { item } = evt;
            graph.setItemState(item, 'active', false);
        });

        graph.on('node:click', (evt) => {
            const { item } = evt;
            graph.setItemState(item, 'selected', true);
        });
        graph.on('canvas:click', (evt) => {
            graph.getNodes().forEach((node) => {
                graph.clearItemStates(node);
            });
        });
    }, []);

    return (
        <div ref={ref}></div>
    )
}

export default ChatBox;