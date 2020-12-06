import 'package:AppAgua/widgets/paginaAgua.dart';
import 'package:flutter/material.dart';
import 'widgets/paginaAgua.dart';
import 'widgets/paginaTodo.dart';
import 'widgets/paginaOutro.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: Text("sua progamanda aque"),
          // DETALHES DA APP BAR VEM AQUE
          bottom: TabBar(tabs: [
            Tab(
              text: 'Agua',
            ),
            Tab(
              text: 'Todo',
            ),
            Tab(
              text: 'outro',
            ),
          ]),
        ),
        body: TabBarView(children: [
          paginaAgua(),
          paginaTodo(),
          paginaOutro(),
        ]),
      ),
    ));
  }
}
