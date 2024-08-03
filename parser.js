const esprima = require('esprima');
const fs = require('fs');

function parseCodeToAST(code) {
  return esprima.parseScript(code, { range: true, loc: true });
}

function findFunctionDefinitions(ast) {
  const functions = [];

  function traverse(node, parent = null, className = null) {
      if (node.type === 'FunctionDeclaration') {
          functions.push({ node, name: node.id.name, className });
      } else if (node.type === 'MethodDefinition' && parent && parent.type === 'ClassBody') {
          functions.push({ node, name: node.key.name, className });
      } else if ((node.type === 'FunctionExpression' || node.type === 'ArrowFunctionExpression') && parent && parent.key) {
          functions.push({ node, name: parent.key.name, className });
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

function buildDependencyGraph(code) {
  const ast = parseCodeToAST(code);
  const functions = findFunctionDefinitions(ast);
  const functionMap = new Map();

  // Map each function to its name and its node in the AST
  functions.forEach(({ node, name, className }) => {
      if (name) {
          if (className !== null) {
              name = `${className}.${name}`;
          }
          functionMap.set(name, { node, className });
      }
  });

  const graph = {};

  // Initialize graph nodes
  functionMap.forEach((func, name) => {
    // console.log(func)
      graph[name] = { start: func.node.loc.start.line, 
                      end: func.node.loc.end.line,
                      class_name: func.className,
                      dependencies: [] };
  });

  // Identify dependencies
  functionMap.forEach((func, name) => {
    const calls = findFunctionCalls(func.node.body);
    calls.forEach(call => {
        const callee = call.callee;
        if (callee.type === 'Identifier' && functionMap.has(callee.name)) {
            graph[name].dependencies.push(callee.name);
            // console.log(callee)
        } else if (callee.type === 'MemberExpression' && callee.object.type === 'Identifier' && functionMap.has(callee.object.name)) {
            graph[name].dependencies.push(callee.object.name);
            // console.log(callee)
        }
    });
  });

  return graph;
}

try {
    const args = process.argv.slice(2);
    arg = args[0]
    const data = fs.readFileSync(arg, 'utf8');

    const graph = buildDependencyGraph(data);

    console.log(JSON.stringify(graph, null, 2));
  } catch (err) {
    console.error('Error reading file:', err);
  }
