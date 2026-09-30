#!/usr/bin/env python3
"""Official AP Calculus curriculum metadata and FRQ bank organization."""
from __future__ import annotations

import json
import re
from pathlib import Path

PART_TOPICS = Path(__file__).with_name("ap_calculus_frq_topics.json")
CLASS_NAMES = {"AB": "Calculus AB", "BC": "Calculus BC"}
SOURCE_URL = "https://apcentral.collegeboard.org/media/pdf/ap-calculus-ab-and-bc-course-and-exam-description.pdf"

UNITS = {
    1: ("Limits and Continuity", {
        "1.1": "Introducing Calculus: Can Change Occur at an Instant?",
        "1.2": "Defining Limits and Using Limit Notation",
        "1.3": "Estimating Limit Values from Graphs",
        "1.4": "Estimating Limit Values from Tables",
        "1.5": "Determining Limits Using Algebraic Properties of Limits",
        "1.6": "Determining Limits Using Algebraic Manipulation",
        "1.7": "Selecting Procedures for Determining Limits",
        "1.8": "Determining Limits Using the Squeeze Theorem",
        "1.9": "Connecting Multiple Representations of Limits",
        "1.10": "Exploring Types of Discontinuities",
        "1.11": "Defining Continuity at a Point",
        "1.12": "Confirming Continuity over an Interval",
        "1.13": "Removing Discontinuities",
        "1.14": "Connecting Infinite Limits and Vertical Asymptotes",
        "1.15": "Connecting Limits at Infinity and Horizontal Asymptotes",
        "1.16": "Working with the Intermediate Value Theorem (IVT)",
    }),
    2: ("Differentiation: Definition and Fundamental Properties", {
        "2.1": "Defining Average and Instantaneous Rates of Change at a Point",
        "2.2": "Defining the Derivative of a Function and Using Derivative Notation",
        "2.3": "Estimating Derivatives of a Function at a Point",
        "2.4": "Connecting Differentiability and Continuity",
        "2.5": "Applying the Power Rule",
        "2.6": "Derivative Rules: Constant, Sum, Difference, and Constant Multiple",
        "2.7": "Derivatives of cos x, sin x, e^x, and ln x",
        "2.8": "The Product Rule",
        "2.9": "The Quotient Rule",
        "2.10": "Derivatives of Tangent, Cotangent, Secant, and Cosecant Functions",
    }),
    3: ("Differentiation: Composite, Implicit, and Inverse Functions", {
        "3.1": "The Chain Rule", "3.2": "Implicit Differentiation",
        "3.3": "Differentiating Inverse Functions",
        "3.4": "Differentiating Inverse Trigonometric Functions",
        "3.5": "Selecting Procedures for Calculating Derivatives",
        "3.6": "Calculating Higher-Order Derivatives",
    }),
    4: ("Contextual Applications of Differentiation", {
        "4.1": "Interpreting the Meaning of the Derivative in Context",
        "4.2": "Straight-Line Motion: Connecting Position, Velocity, and Acceleration",
        "4.3": "Rates of Change in Applied Contexts Other Than Motion",
        "4.4": "Introduction to Related Rates", "4.5": "Solving Related Rates Problems",
        "4.6": "Approximating Values of a Function Using Local Linearity and Linearization",
        "4.7": "Using L'Hospital's Rule for Determining Limits of Indeterminate Forms",
    }),
    5: ("Analytical Applications of Differentiation", {
        "5.1": "Using the Mean Value Theorem",
        "5.2": "Extreme Value Theorem, Global Versus Local Extrema, and Critical Points",
        "5.3": "Determining Intervals on Which a Function Is Increasing or Decreasing",
        "5.4": "Using the First Derivative Test to Determine Relative Extrema",
        "5.5": "Using the Candidates Test to Determine Absolute Extrema",
        "5.6": "Determining Concavity of Functions over Their Domains",
        "5.7": "Using the Second Derivative Test to Determine Extrema",
        "5.8": "Sketching Graphs of Functions and Their Derivatives",
        "5.9": "Connecting a Function, Its First Derivative, and Its Second Derivative",
        "5.10": "Introduction to Optimization Problems", "5.11": "Solving Optimization Problems",
        "5.12": "Exploring Behaviors of Implicit Relations",
    }),
    6: ("Integration and Accumulation of Change", {
        "6.1": "Exploring Accumulations of Change", "6.2": "Approximating Areas with Riemann Sums",
        "6.3": "Riemann Sums, Summation Notation, and Definite Integral Notation",
        "6.4": "The Fundamental Theorem of Calculus and Accumulation Functions",
        "6.5": "Interpreting the Behavior of Accumulation Functions Involving Area",
        "6.6": "Applying Properties of Definite Integrals",
        "6.7": "The Fundamental Theorem of Calculus and Definite Integrals",
        "6.8": "Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation",
        "6.9": "Integrating Using Substitution", "6.10": "Integrating Using Long Division and Completing the Square",
        "6.11": "Integrating Using Integration by Parts", "6.12": "Integrating Using Linear Partial Fractions",
        "6.13": "Evaluating Improper Integrals", "6.14": "Selecting Techniques for Antidifferentiation",
    }),
    7: ("Differential Equations", {
        "7.1": "Modeling Situations with Differential Equations",
        "7.2": "Verifying Solutions for Differential Equations", "7.3": "Sketching Slope Fields",
        "7.4": "Reasoning Using Slope Fields", "7.5": "Approximating Solutions Using Euler's Method",
        "7.6": "Finding General Solutions Using Separation of Variables",
        "7.7": "Finding Particular Solutions Using Initial Conditions and Separation of Variables",
        "7.8": "Exponential Models with Differential Equations",
        "7.9": "Logistic Models with Differential Equations",
    }),
    8: ("Applications of Integration", {
        "8.1": "Finding the Average Value of a Function on an Interval",
        "8.2": "Connecting Position, Velocity, and Acceleration Using Integrals",
        "8.3": "Using Accumulation Functions and Definite Integrals in Applied Contexts",
        "8.4": "Finding the Area Between Curves Expressed as Functions of x",
        "8.5": "Finding the Area Between Curves Expressed as Functions of y",
        "8.6": "Finding the Area Between Curves That Intersect at More Than Two Points",
        "8.7": "Volumes with Cross Sections: Squares and Rectangles",
        "8.8": "Volumes with Cross Sections: Triangles and Semicircles",
        "8.9": "Volume with Disc Method: Revolving Around the x- or y-Axis",
        "8.10": "Volume with Disc Method: Revolving Around Other Axes",
        "8.11": "Volume with Washer Method: Revolving Around the x- or y-Axis",
        "8.12": "Volume with Washer Method: Revolving Around Other Axes",
        "8.13": "Arc Length of a Smooth, Planar Curve and Distance Traveled",
    }),
    9: ("Parametric Equations, Polar Coordinates, and Vector-Valued Functions", {
        "9.1": "Defining and Differentiating Parametric Equations",
        "9.2": "Second Derivatives of Parametric Equations",
        "9.3": "Finding Arc Lengths of Curves Given by Parametric Equations",
        "9.4": "Defining and Differentiating Vector-Valued Functions",
        "9.5": "Integrating Vector-Valued Functions",
        "9.6": "Solving Motion Problems Using Parametric and Vector-Valued Functions",
        "9.7": "Defining Polar Coordinates and Differentiating in Polar Form",
        "9.8": "Area of a Polar Region or Area Bounded by a Single Polar Curve",
        "9.9": "Area of the Region Bounded by Two Polar Curves",
    }),
    10: ("Infinite Sequences and Series", {
        "10.1": "Defining Convergent and Divergent Infinite Series", "10.2": "Working with Geometric Series",
        "10.3": "The nth Term Test for Divergence", "10.4": "Integral Test for Convergence",
        "10.5": "Harmonic Series and p-Series", "10.6": "Comparison Tests for Convergence",
        "10.7": "Alternating Series Test for Convergence", "10.8": "Ratio Test for Convergence",
        "10.9": "Determining Absolute or Conditional Convergence", "10.10": "Alternating Series Error Bound",
        "10.11": "Finding Taylor Polynomial Approximations of Functions", "10.12": "Lagrange Error Bound",
        "10.13": "Radius and Interval of Convergence of Power Series",
        "10.14": "Finding Taylor or Maclaurin Series for a Function",
        "10.15": "Representing Functions as Power Series",
    }),
}

BC_ONLY = {f"9.{n}" for n in range(1, 10)} | {f"10.{n}" for n in range(1, 16)} | {"6.11", "6.12", "6.13", "7.5", "7.9", "8.13"}
TOPIC_NAMES = {topic: name for _, topics in UNITS.values() for topic, name in topics.items()}


def curriculum(course: str) -> list[dict]:
    maximum = 8 if course.upper() == "AB" else 10
    return [{"id": f"ap-unit-{number}", "name": f"Unit {number}: {UNITS[number][0]}",
             "sections": [{"id": f"ap-topic-{topic.replace('.', '-')}", "name": f"{topic} {name}"}
                          for topic, name in UNITS[number][1].items() if course.upper() == "BC" or topic not in BC_ONLY]}
            for number in range(1, maximum + 1)]


def topic_key(topic: str) -> tuple[int, int]:
    unit, number = topic.split(".")
    return int(unit), int(number)


def load_part_topics(path: Path = PART_TOPICS) -> dict[str, dict[str, str | None]]:
    return json.loads(path.read_text())["questions"]


def section_topic(qid: str, parts: dict[str, str | None]) -> str:
    """The last CED topic a question reaches: its highest-numbered part topic."""
    course = qid.split("-")[2].upper()
    topics = [topic for topic in parts.values() if topic is not None]
    if not topics:
        raise ValueError(f"{qid}: no part has a CED topic")
    for topic in topics:
        if topic not in TOPIC_NAMES:
            raise ValueError(f"{qid}: unknown CED topic {topic}")
        if course == "AB" and topic in BC_ONLY:
            raise ValueError(f"{qid}: AB question assigned BC-only topic {topic}")
    return max(topics, key=topic_key)


def exam_tags(qid: str) -> list[str]:
    """Year, Form B, and the Section II part with its calculator rule.

    Part A (graphing calculator required) was questions 1-3 through 2010 and
    questions 1-2 from 2011; the rest are Part B (no calculator). Verified
    against the "SECTION II, Part B" page of every source PDF with a text layer.
    """
    match = re.fullmatch(r"ap-calc-(?:ab|bc)-(\d{4})(-form-b)?-frq-(\d+)", qid)
    if not match:
        raise ValueError(f"Unrecognized AP question id: {qid}")
    year, form_b, number = int(match[1]), bool(match[2]), int(match[3])
    part_a = number <= (3 if year <= 2010 else 2)
    return [str(year)] + (["Form B"] if form_b else []) + (
        ["Part A", "Calculator Active"] if part_a else ["Part B", "No Calculator"])


def course_classes() -> list[dict]:
    return [{"id": f"ap-calculus-{course.lower()}", "name": CLASS_NAMES[course], "units": curriculum(course)}
            for course in ("AB", "BC")]


def organize(qid: str, parts: dict[str, str | None]) -> dict:
    """Class, unit, section and tags for one question, in both bank formats' terms."""
    course = qid.split("-")[2].upper()
    topic = section_topic(qid, parts)
    unit = int(topic.split(".")[0])
    return {"classId": f"ap-calculus-{course.lower()}", "className": CLASS_NAMES[course],
            "unitId": f"ap-unit-{unit}", "unitName": f"Unit {unit}: {UNITS[unit][0]}",
            "sectionId": f"ap-topic-{topic.replace('.', '-')}", "sectionName": f"{topic} {TOPIC_NAMES[topic]}",
            "tags": exam_tags(qid)}
