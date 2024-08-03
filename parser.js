const esprima = require('esprima');
const fs = require('fs');

function parseCodeToAST(code) {
  return esprima.parseScript(code, { range: true, loc: true });
}

function findFunctionDefinitions(ast) {
  const functions = [];

  function traverse(node, parent = null) {
      if (node.type === 'FunctionDeclaration') {
          functions.push({ node, name: node.id.name });
      } else if ((node.type === 'FunctionExpression' || node.type === 'ArrowFunctionExpression') && parent && parent.key) {
          functions.push({ node, name: parent.key.name });
      }

      for (let key in node) {
          if (node[key] && typeof node[key] === 'object' && key !== 'parent') {
              traverse(node[key], node);
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
  functions.forEach(({ node, name }) => {
      if (name) {
          functionMap.set(name, node);
      }
  });

  const graph = {};

  // Initialize graph nodes
  functionMap.forEach((func, name) => {
    console.log(func, name)
      graph[name] = { start: func.loc.start.line, 
                      end: func.loc.end.line,
                      dependencies: [] };
  });

  // Identify dependencies
  functionMap.forEach((func, name) => {
    const calls = findFunctionCalls(func.body);
    calls.forEach(call => {
        const callee = call.callee;
        if (callee.type === 'Identifier' && functionMap.has(callee.name)) {
            graph[name].dependencies.push(callee.name);
        } else if (callee.type === 'MemberExpression' && callee.object.type === 'Identifier' && functionMap.has(callee.object.name)) {
            graph[name].dependencies.push(callee.object.name);
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
