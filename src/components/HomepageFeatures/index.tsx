// import type { ReactNode } from 'react';
// import clsx from 'clsx';
// import Heading from '@theme/Heading';
// import styles from './styles.module.css';
// import Link from '@docusaurus/Link';

// type FeatureItem = {
//   title: string;
//   Svg: React.ComponentType<React.ComponentProps<'svg'>>;
//   description: ReactNode;
//   to: string;
// };

// const FeatureList: FeatureItem[] = [
//   {
//     title: 'Module 1: The Robotic Nervous System (ROS 2)',
//     Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
//     description: (
//       <>
//         Master the Robot Operating System (ROS 2), the foundational communication layer for building complex, modular robot applications.
//       </>
//     ),
//     to: '/ai-book/module1-ros2/1-1-introduction',
//   },
//   {
//     title: 'Module 2: The Digital Twin (Gazebo & Unity)',
//     Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
//     description: (
//       <>
//         Learn to build and use high-fidelity simulations in Gazebo and Unity to test, validate, and train your robot in a virtual environment.
//       </>
//     ),
//     to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
//   },
//   {
//     title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
//     Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
//     description: (
//       <>
//         Dive into AI-powered perception using NVIDIA Isaac, generating synthetic data and deploying hardware-accelerated computer vision pipelines.
//       </>
//     ),
//     to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
//   },
//   {
//     title: 'Module 4: Vision-Language-Action (VLA)',
//     Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
//     description: (
//       <>
//         Integrate Large Language Models (LLMs) to create robots that understand and respond to natural language commands, bridging the gap between human intent and robot action.
//       </>
//     ),
//     to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
//   },
// ];

// function Feature({ title, Svg, description, to }: FeatureItem) {
//   return (
//     <div className={clsx('col col--6', styles.featureCard)}>
//       <div className="card">
//         <div className="card__header text--center">
//           <Svg className={styles.featureSvg} role="img" />
//         </div>
//         <div className="card__body text--center padding-horiz--md">
//           <Heading as="h3">{title}</Heading>
//           <p>{description}</p>
//         </div>
//         <div className="card__footer">
//           <Link
//             className="button button--primary button--block"
//             to={to}>
//             Go to Module
//           </Link>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default function HomepageFeatures(): ReactNode {
//   return (
//     <section className={styles.features}>
//       <div className="container">
//         <div className="row">
//           {FeatureList.map((props, idx) => (
//             <Feature key={idx} {...props} />
//           ))}
//         </div>
//       </div>
//     </section>
//   );
// }



import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

type FeatureItem = {
  title: string;
  description: ReactNode;
  to: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description: (
      <>
        Master the Robot Operating System (ROS 2), the foundational communication layer for building complex, modular robot applications.
      </>
    ),
    to: '/ai-book/module1-ros2/1-1-introduction',
  },
  {
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description: (
      <>
        Learn to build and use high-fidelity simulations in Gazebo and Unity to test, validate, and train your robot in a virtual environment.
      </>
    ),
    to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
  },
  {
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
    description: (
      <>
        Dive into AI-powered perception using NVIDIA Isaac, generating synthetic data and deploying hardware-accelerated computer vision pipelines.
      </>
    ),
    to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: (
      <>
        Integrate Large Language Models (LLMs) to create robots that understand and respond to natural language commands, bridging the gap between human intent and robot action.
      </>
    ),
    to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
  },
];

function Feature({ title, description, to }: FeatureItem) {
  return (
    <div className={clsx('col col--6', styles.featureCard)}>
      <div className="card">
        <div className="card__body text--center padding-horiz--md">
          <Heading as="h3">{title}</Heading>
          <p>{description}</p>
        </div>
        <div className="card__footer">
          <Link
            className="button button--primary button--block"
            to={to}>
            Go to Module
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="text--center">
          <Heading as="h2">Explore our learning modules</Heading>
        </div>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

