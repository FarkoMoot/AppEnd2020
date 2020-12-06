import 'package:flutter/material.dart';

class paginaAgua extends StatefulWidget {
  @override
  _paginaAguaState createState() => _paginaAguaState();
}

class _paginaAguaState extends State<paginaAgua> {
  @override
  void setState(fn) {
    // TODO: implement setState
    super.setState(fn);
  }
  
  var test = [];

  void funcONE() {
    print(test);

    test.add(1);
    this.setState(() {
      test = 
    });
    print(test);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        FloatingActionButton(
          onPressed: funcONE,
          tooltip: 'Increment',
          child: Icon(Icons.add),
        ),
      ],
    );
  }
}
