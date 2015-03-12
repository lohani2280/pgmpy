#!/usr/bin/env python
import unittest
from io import StringIO
import networkx as nx
from pgmpy.readwrite import ProbModelXMLWriter, ProbModelXMLReader, parse_probmodelxml, generate_probmodelxml
import warnings
try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
        except ImportError:
            warnings.warn("Failed to import ElementTree from any known place")


class TestProbModelXMLReaderString(unittest.TestCase):
    def setUp(self):
        string = """<ProbModelXML formatVersion="1.0">
      <ProbNet type="BayesianNetwork">
        <AdditionalConstraints />
        <Comment>Student example model from Probabilistic Graphical Models: Principles and Techniques by Daphne Koller</Comment>
        <Language>
            English
        </Language>
        <AdditionalProperties />
        <Variables>
            <Variable name="intelligence" type="FiniteState" role="Chance">
                <Comment />
                <Coordinates />
                <AdditionalProperties />
                <States>
                    <State name="smart"><AdditionalProperties /></State>
                    <State name="dumb"><AdditionalProperties /></State>
                </States>
            </Variable>
            <Variable name="difficulty" type="FiniteState" role="Chance">
                <Comment />
                <Coordinates />
                <AdditionalProperties />
                <States>
                    <State name="difficult"><AdditionalProperties /></State>
                    <State name="easy"><AdditionalProperties /></State>
                </States>
            </Variable>
        </Variables>
        <Links>
            <Link var1="difficulty" var2="grade" directed="1">
                <Comment>Directed Edge from difficulty to grade</Comment>
                <Label>diff_to_grad</Label>
                <AdditionalProperties />
            </Link>
            <Link var1="intelligence" var2="grade" directed="1">
                <Comment>Directed Edge from intelligence to grade</Comment>
                <Label>intel_to_grad</Label>
                <AdditionalProperties />
            </Link>
            <Link var1="intelligence" var2="SAT" directed="1">
                <Comment>Directed Edge from intelligence to SAT</Comment>
                <Label>intel_to_sat</Label>
                <AdditionalProperties />
            </Link>
            <Link var1="grade" var2="recommendation_letter" directed="1">
                <Comment>Directed Edge from grade to recommendation_letter</Comment>
                <Label>grad_to_reco</Label>
                <AdditionalProperties />
            </Link>
        </Links>
	<Potential type="Table" role="ConditionalProbability" label="string">
            <Comment>CPDs in the form of table</Comment>
            <AdditionalProperties />
        </Potential>
    </ProbNet>
    <Policies />
    <InferenceOptions />
</ProbModelXML>
"""
        self.reader_string = ProbModelXMLReader(string=string)
        self.reader_file = ProbModelXMLReader(path=StringIO(string))

    def test_comment(self):
        comment_expected = "Student example model from Probabilistic Graphical Models: Principles and Techniques by Daphne Koller"
        self.maxDiff = None
        self.assertEqual(self.reader_string.probnet['comment'], comment_expected)
        self.assertEqual(self.reader_file.probnet['comment'], comment_expected)

    def test_variables(self):
        variables_expected = {'difficulty':
				{'type': 'FiniteState',
				 'States': {'easy': {}, 'difficult': {}},
				 'Comment': None,
				 'role': 'Chance',
				 'Coordinates': {}
				},
			      'intelligence':
				{'type': 'FiniteState',
				 'States': {'dumb': {}, 'smart': {}},
				 'Comment': None,
				 'role': 'Chance',
				 'Coordinates': {}}
			     }
        self.maxDiff = None
        self.assertEqual(self.reader_string.probnet['Variables'], variables_expected)
        self.assertEqual(self.reader_file.probnet['Variables'], variables_expected)

    def test_edges(self):
        edges_expected = {('difficulty', 'grade'):
			    {'Label': 'diff_to_grad',
			     'directed': '1',
			     'Comment': 'Directed Edge from difficulty to grade'
			    },
			  ('intelligence', 'SAT'):
			    {'Label': 'intel_to_sat',
			     'directed': '1',
			     'Comment': 'Directed Edge from intelligence to SAT'
			    },
			  ('grade', 'recommendation_letter'):
			    {'Label': 'grad_to_reco',
			     'directed': '1',
			     'Comment': 'Directed Edge from grade to recommendation_letter'
			    },
			  ('intelligence', 'grade'):
			    {'Label': 'intel_to_grad',
			     'directed': '1',
			     'Comment': 'Directed Edge from intelligence to grade'
			    }
			 }
        self.maxDiff = None
        self.assertEqual(self.reader_string.probnet['edges'], edges_expected)
        self.assertEqual(self.reader_file.probnet['edges'], edges_expected)
