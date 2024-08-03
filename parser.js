const esprima = require('esprima');
const fs = require('fs');

function parseCodeToAST(code) {
  return esprima.parseScript(code, { range: true, loc: true });
}

function findFunctionDefinitions(ast, path) {
  const functions = [];

  function traverse(node, parent = null, className = null) {
      if (node.type === 'FunctionDeclaration') {
          functions.push({ node, name: node.id.name, className, path: path });
      } else if (node.type === 'MethodDefinition' && parent && parent.type === 'ClassBody') {
          functions.push({ node, name: node.key.name, className, path: path });
      } else if ((node.type === 'FunctionExpression' || node.type === 'ArrowFunctionExpression') && parent && parent.key) {
          functions.push({ node, name: parent.key.name, className, path: path });
      }

      if (node.type === 'ClassDeclaration') {
          className = node.id.name;
      }

      for (let key in node) {
          if (node[key] && typeof node[key] === 'object' && key !== 'parent') {
              traverse(node[key], node, className);
          }
      }
  }

  traverse(ast);
  return functions;
}

function findFunctionCalls(node) {
  const calls = [];

  function traverse(node) {
      if (node.type === 'CallExpression') {
          calls.push(node);
      }

      for (let key in node) {
          if (node[key] && typeof node[key] === 'object' && key !== 'parent') {
              traverse(node[key]);
          }
      }
  }

  traverse(node);
  return calls;
}

function buildDependencyGraph(paths) {
  let functions = [];
  for (const path of paths) {
    const code = fs.readFileSync(path, 'utf8');
    const ast = parseCodeToAST(code);
    const defs = findFunctionDefinitions(ast, path);
    functions = functions.concat(defs);
  }

  const functionMap = new Map();

  // Map each function to its name and its node in the AST
  functions.forEach(({ node, name, className, path }) => {
      if (name) {
          if (className !== null) {
              name = `${className}.${name}`;
          }
          functionMap.set(name, { node, className, path });
      }
  });

  const graph = {};

  // Initialize graph nodes
  functionMap.forEach((func, name) => {
      graph[name] = { start: func.node.loc.start.line, 
                      end: func.node.loc.end.line,
                      class_name: func.className,
                      path: func.path,
                      dependencies: [] };
  });

  // Identify dependencies
  functionMap.forEach((func, name) => {
    const calls = findFunctionCalls(func.node.body);
    calls.forEach(call => {
        const callee = call.callee;
        if (callee.type === 'Identifier' && functionMap.has(callee.name)) {
            // graph[name].dependencies.push(callee.name);
            graph[name].dependencies.push({
              name: callee.name,
              path: func.path,
              start: call.loc.start.line,
              end: call.loc.end.line
            })
            // console.log("hello", call);
        } else if (callee.type === 'MemberExpression' && callee.object.type === 'Identifier' && functionMap.has(callee.object.name)) {
            // graph[name].dependencies.push(callee.object.name);
            graph[name].dependencies.push({
              name: callee.object.name,
              path: func.path,
              start: call.loc.start.line,
              end: call.loc.end.line
            })
        }
    });
  });

  return graph;
}

try {
    const args = process.argv.slice(2);
    const graph = buildDependencyGraph(args);

    console.log(JSON.stringify(graph, null, 2));
  } catch (err) {
    console.error('Error reading file:', err);
  }
